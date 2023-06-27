import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from ..views import sendAPOD, storeMessageWeekly, sendBackUpMessage


def start():
    scheduler = BackgroundScheduler()
    # schedule the sendAPOD function to run every day at 12:05:00
    scheduler.add_job(sendAPOD, 'cron', hour=9,minute=37,second=0)
    scheduler.add_job(storeMessageWeekly, trigger=CronTrigger(day_of_week='mon', hour=9, minute=37, second=0)) 
    print("running scheduled job........", datetime.datetime.now()) 

    try:
        scheduler.start()
    except Exception as exception:
        scheduler.shutdown()
        print("Scheduler stopped")
