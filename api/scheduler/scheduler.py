import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from ..views import sendAPOD, storeMessageWeekly


def start():
    scheduler = BackgroundScheduler()
    # schedule the sendAPOD function to run every day at 12:05:00
    scheduler.add_job(sendAPOD, 'cron', hour=12, minute=5, second=0)
    scheduler.add_job(storeMessageWeekly, 'cron', day_of_week='mon', hour=13, minute=5, second=0)
    print("running scheduled job........", datetime.datetime.now()) 

    scheduler.start()
