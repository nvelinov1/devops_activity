import requests
from smtplib import SMTP
from email.mime.text import MIMEText
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError, Timeout

app = Flask(__name__)

def send_email():

    from_addr = "devops@activity.net"
    to_addr = "nikolavelinov65@gmail.com"

    subj = "WEBPAGE ERROR"

    message_text = "Fatal error: URL failed to return expected response"

    message = MIMEText(message_text, "plain")
    message["Subject"] = subj
    message["From"] = from_addr
    message["To"] = to_addr

    with SMTP('mail.mysmtp.com', '25') as server:
        server.login('myuser', 'secret')
        server.sendmail(from_addr, to_addr, message.as_string())

def monitor_job():
    try:
        res = requests.get("http://web:5000/", timeout=10)
    except (MaxRetryError, ConnectionError, Timeout):
        print("connection error")
        send_email()
        return
    if res.status_code != 200:
        print("status code error")
        send_email()

def schedule_job():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(monitor_job,'interval',seconds=60)
    sched.start()


schedule_job()
app.run(port=8010, use_reloader=False)