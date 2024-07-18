import requests

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError, Timeout

app = Flask(__name__)

def monitor_job():
    try:
        res = requests.get("http://web:5000/", timeout=10)
    except (MaxRetryError, ConnectionError, Timeout):
        print("timeout error")
        return
    if res.status_code != 200:
        print("wrong status code error")

def schedule_job():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(monitor_job,'interval',seconds=60)
    sched.start()


schedule_job()
app.run(port=8010, use_reloader=False)