import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from ..views import sendAPOD


def start():
    scheduler = BackgroundScheduler()
    # schedule the sendAPOD function to run every day at 12:05:00
    scheduler.add_job(sendAPOD, 'cron', hour=12,minute=0,second=0)
    print("running scheduled job........", datetime.datetime.now()) 
    scheduler.start()
