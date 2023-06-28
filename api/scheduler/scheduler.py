import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from ..views import send_NASA_APOD, store_message_weekly


def start():
    scheduler = BackgroundScheduler()
    # schedule the sendAPOD function to run every day at 12:05:00
    scheduler.add_job(send_NASA_APOD, 'cron', hour=12, minute=5, second=0)
    # schedule the store_message_weekly function to run every monday at 13:05:00
    scheduler.add_job(store_message_weekly, 'cron', day_of_week='mon', hour=13, minute=5, second=0)
    print("running scheduled job........", datetime.datetime.now()) 

    scheduler.start()
