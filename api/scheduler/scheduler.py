from apscheduler.schedulers.background import BackgroundScheduler
from ..views import sendAPOD


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sendAPOD, 'interval', hours=24)
    scheduler.start()