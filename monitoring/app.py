import requests
import os
from smtplib import SMTP
from dotenv import load_dotenv
from email.mime.text import MIMEText
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError, Timeout

load_dotenv('./.env')
SMTP_ADDRESS=os.environ.get("SMARTHOST_ADDRESS")
SMTP_USER=os.environ.get("SMARTHOST_USER")
SMTP_PASS=os.environ.get("SMARTHOST_PASSWORD")
SMTP_TO=os.environ.get("SMTP_TO")
SMTP_FROM=os.environ.get("SMTP_FROM")
REQ_URL=os.environ.get("REQ_URL")
REQ_TIMEOUT=int(os.environ.get("REQ_TIMEOUT"))
REQ_INTERVAL=int(os.environ.get("REQ_INTERVAL"))


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

    with SMTP(SMTP_ADDRESS, '25') as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(from_addr, to_addr, message.as_string())

def monitor_job():
    try:
        res = requests.get(REQ_URL, timeout=REQ_TIMEOUT)
    except (MaxRetryError, ConnectionError, Timeout):
        print("connection error")
        send_email()
        return
    if res.status_code != 200:
        print("status code error")
        send_email()

def schedule_job():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(monitor_job,'interval',seconds=REQ_INTERVAL)
    sched.start()


schedule_job()
app.run(port=8010, use_reloader=False)