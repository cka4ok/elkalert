from time import sleep
from config import CONFIG
from elastic import GetElastAlerts
from receivers.email import SendEmails


if __name__ == "__main__":
    print(CONFIG)
    elast_alerts = GetElastAlerts(**CONFIG["elasticsearch"])
    send_emails = SendEmails(**CONFIG["email"])

    while True:
        alerts = elast_alerts.get_elastic_alerts()
        print(alerts)
        send_emails.send_messages(alerts, verbose=True)
        sleep(20)



