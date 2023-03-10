from apscheduler.schedulers.background import BackgroundScheduler
from ..views import sendAPOD


def start():
    scheduler = BackgroundScheduler()
    # schedule the sendAPOD function to run every day at 12:05:00
    scheduler.add_job(sendAPOD, 'cron', hour=12,minute=5,second=0) #could add a logger here
    scheduler.start()