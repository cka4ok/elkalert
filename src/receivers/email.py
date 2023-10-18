import smtplib
from email.message import EmailMessage
from time import sleep

class SendEmails:
    def __init__(self, sender, server, port=25, tls=False, 
                 user=None, password=None, timeout=None, email_groups=None):
        self.sender = sender
        self.server = server
        self.port = port
        self.tls = tls
        self.user = user
        self.password = password
        self.timeout = timeout
        self.email_groups = email_groups

    def __extract_email_groups(self, raw_to):
        to = []
        for item in raw_to:
            if "@" in item:
                to.append(item)
            elif item in self.email_groups:
                to.extend(self.email_groups[item])
        return list(set(to))
    
   
    def __extract_messages(self, alerts):
        messages = []
        for alert in alerts:
            if ("email" in alert["elkalert"]) and alert["elkalert"]["to"]:
                msg_to = alert["elkalert"]["to"]
                if (alert["elkalert"]["subject"] or alert["elkalert"]["subject"] != "auto"):
                    msg_subject = alert["elkalert"]["subject"]
                else:
                    msg_subject = alert["rule"]["name"]

                if alert["elkalert"]["body"] or alert["elkalert"]["body"] != "auto":
                    msg_body = alert["elkalert"]["body"] 
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
    
    def send_messages(self, alerts):
        messages = self.__extract_messages(alerts)
        if messages:
            srv_connect = smtplib.SMTP(self.server, self.port)
            if self.tls:
                srv_connect.starttls()
            if self.user:
                srv_connect.login(self.user, self.password)

            for msg in messages:
                self.__send_message(srv_connect, **msg)
                if self.timeout: sleep(self.timeout)

            srv_connect.quit()