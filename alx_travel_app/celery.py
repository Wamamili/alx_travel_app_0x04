import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

# Create Celery app
app = Celery('alx_travel_app')

# Load configuration from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Optional: Define periodic tasks here if needed
app.conf.beat_schedule = {
    # Example: send-email-every-hour
    # 'send-emails': {
    #     'task': 'listings.tasks.send_booking_confirmation_email',
    #     'schedule': crontab(minute=0),  # Every hour
    # },
}


@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery setup."""
    print(f'Request: {self.request!r}')