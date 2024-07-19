import requests
import os
from smtplib import SMTP
from dotenv import load_dotenv
from email.mime.text import MIMEText
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError, Timeout

#Read environment variables from .env
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

    from_addr = SMTP_FROM
    to_addr = SMTP_TO

    subj = "WEBPAGE ERROR"

    message_text = "Fatal error: URL failed to return expected response"

    #Create a MimeText object with the required params
    message = MIMEText(message_text, "plain")
    message["Subject"] = subj
    message["From"] = from_addr
    message["To"] = to_addr

    #Send the email using the required hostname/credentials and message params
    with SMTP(SMTP_ADDRESS, '25') as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(from_addr, to_addr, message.as_string())

def monitor_job():
    try:
        #Send a request to the required URL while including the timeout parameter
        res = requests.get(REQ_URL, timeout=REQ_TIMEOUT)
    #Add exception catching for the following situations: unable to connect, timeout, max retry
    except (MaxRetryError, ConnectionError, Timeout):
        #Print an error message and execute the send_email() function
        print("connection error")
        send_email()
        return
    #If a response is returned with a non-200 status code, print an error message and send the email
    if res.status_code != 200:
        print("status code error")
        send_email()

def schedule_job():
    #Add a scheduled job at the required interval
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(monitor_job,'interval',seconds=REQ_INTERVAL)
    sched.start()

#Schedule the job once the application is run, and run the Flask application on port 8010
schedule_job()
app.run(port=8010, use_reloader=False)