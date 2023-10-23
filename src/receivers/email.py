import smtplib
from email.message import EmailMessage
from time import sleep

class SendEmails:
    def __init__(self, sender, server, port=25, tls=False, 
                 user=None, password=None, timeout=None, recipient_groups=None):
        self.sender = sender
        self.server = server
        self.port = port
        self.tls = tls
        self.user = user
        self.password = password
        self.timeout = timeout
        self.recipient_groups = recipient_groups

    def __extract_email_groups(self, raw_to):
        to = []
        for item in raw_to:
            if "@" in item:
                to.append(item)
            elif item in self.recipient_groups:
                to.extend(self.recipient_groups[item])
        return list(set(to))
    
   
    def __extract_messages(self, alerts):
        messages = []
        for alert in alerts:
            alert = alert["_source"]
            if "email" in alert["elkalert"] and alert["elkalert"]["email"]["to"]:
                email = alert["elkalert"]["email"]
                msg_to = email["to"]
                if email["subject"] and email["subject"] != "auto":
                    msg_subject = email["subject"]
                else:
                    msg_subject = alert["kibana"]["alert"]["actionGroupName"] + ": " + alert["rule"]["name"]

                if email["body"] and email["body"] != "auto":
                    msg_body = email["body"] 
                else:
                    msg_body = alert["message"] if "message" in alert else ""
                
                messages.append({"to": msg_to, "subject": msg_subject, "body": msg_body})
        return messages

    def __send_message(self, srv_connect, to, subject, body, verbose=False):
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = ", ".join(self.__extract_email_groups(to))
        msg['from'] = self.sender
        if verbose:
            print(msg)
        srv_connect.send_message(msg)

    
    def send_messages(self, alerts, verbose=False):
        messages = self.__extract_messages(alerts)
        if messages:
            try:
                srv_connect = smtplib.SMTP(self.server, self.port)
                if self.tls:
                    srv_connect.starttls()
                if self.user:
                    srv_connect.login(self.user, self.password)

                for msg in messages:
                    self.__send_message(srv_connect, **msg, verbose=verbose)
                    if self.timeout: sleep(self.timeout)
                srv_connect.quit()
            except Exception as error:
                print(error)