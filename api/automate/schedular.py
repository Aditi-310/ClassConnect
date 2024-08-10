from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import call_command
from apscheduler.triggers.interval import IntervalTrigger

import logging

logger = logging.getLogger('api')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: call_command('send_reminders'),
        trigger=CronTrigger(hour="6",minute="0"),
        # trigger=IntervalTrigger(seconds=30), #for testing and try using command ->  python manage.py send_reminders
        id='send_reminders',
        max_instances=1,
        replace_existing=True
    )
    scheduler.start()
    logger.info("Scheduler started")



