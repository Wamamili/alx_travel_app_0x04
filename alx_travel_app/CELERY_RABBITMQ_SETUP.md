# Celery & RabbitMQ Setup Guide for PythonAnywhere

## Overview

This guide explains how to set up Celery with RabbitMQ on PythonAnywhere to handle background tasks like sending emails and processing payments.

**Requirements:**
- PythonAnywhere **Paid Account** (free tier doesn't support RabbitMQ)
- Recommended: Starter tier ($5+/month) or higher

## Step 1: Enable RabbitMQ on PythonAnywhere

1. Log in to your PythonAnywhere account
2. Go to **Account** → **Messaging** (or **Services**)
3. Click **Enable RabbitMQ**
4. Note down the RabbitMQ connection details:
   - **AMQP URL**: `amqp://username:password@hostname:port//`
   - **Username**: Your PythonAnywhere username
   - **Password**: Auto-generated (shown on the page)

Example:
```
amqp://myusername:abc123def456@myusername.rabbitmq.pythonanywhere-services.com:5672//
```

## Step 2: Update Environment Variables

Add these to your `.env` file:

```bash
nano .env
```

Add/Update:
```
# Celery Configuration
CELERY_BROKER_URL=amqp://username:password@hostname:5672//
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

Replace credentials with your RabbitMQ connection details.

Save: `Ctrl+X` → `Y` → `Enter`

## Step 3: Install Dependencies

In your bash console (with virtualenv activated):

```bash
workon alx_travel_app
pip install -r requirements.txt
```

Key packages:
- `celery==5.3.4`
- `kombu==5.3.4` (RabbitMQ support)
- `redis==5.0.1` (Result backend)

## Step 4: Test Celery Locally (Optional)

Before deploying, test Celery locally:

```bash
# Terminal 1: Start Celery worker
celery -A alx_travel_app worker -l info

# Terminal 2: Start Celery Beat (scheduler)
celery -A alx_travel_app beat -l info

# Terminal 3: Django shell
python manage.py shell

# In shell:
from listings.tasks import debug_task
result = debug_task.delay()
print(result.get())  # Should print success message
```

## Step 5: Deploy Worker on PythonAnywhere

### Option A: Always-On Web Worker (Recommended for low traffic)

1. Go to **Web** tab
2. Add a new scheduled task:
   - **Time**: Every hour
   - **Command**: `celery -A alx_travel_app worker -l info`
   - **Working directory**: `/home/username/alx_travel_app_0x04/alx_travel_app`

### Option B: Background Worker Task (Best for production)

PythonAnywhere Paid accounts support long-running background tasks:

1. Go to **Tasks** tab
2. Click **Add new background worker task**
3. Fill in:
   - **Name**: `celery_worker`
   - **Command**: 
   ```
   celery -A alx_travel_app worker -l info --time-limit=600
   ```
   - **Working directory**: `/home/username/alx_travel_app_0x04/alx_travel_app`
   - **Virtualenv**: `/home/username/.virtualenvs/alx_travel_app`
   - **CPU cores**: 1 (or more if available)

4. Click **Create**

The worker will run continuously and process tasks from RabbitMQ queue.

## Step 6: Deploy Celery Beat (Task Scheduler)

Celery Beat runs periodic tasks (like sending reminders hourly, cleanup daily).

1. Go to **Tasks** tab
2. Click **Add new background worker task**
3. Fill in:
   - **Name**: `celery_beat`
   - **Command**: 
   ```
   celery -A alx_travel_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```
   - **Working directory**: `/home/username/alx_travel_app_0x04/alx_travel_app`
   - **Virtualenv**: `/home/username/.virtualenvs/alx_travel_app`
   - **CPU cores**: 1

4. Click **Create**

⚠️ **Important:** Only run ONE instance of Celery Beat to avoid duplicate tasks.

## Step 7: Verify Celery Connection

In your bash console:

```bash
# Test RabbitMQ connection
python manage.py shell
>>> from celery import current_app
>>> current_app.connection()  # Should connect without errors
>>> 

# Test email task
from listings.tasks import send_booking_confirmation_email
task = send_booking_confirmation_email.delay(
    1,  # booking_id
    'test@example.com',
    'John Doe',
    'Luxury Beach Villa',
    '2025-11-20',
    '2025-11-25'
)
print(task.id)  # Task ID
print(task.status)  # Should be 'PENDING' or 'STARTED'
```

## Step 8: Monitor Tasks

### View Task Queue Status

```bash
# In Django shell
from celery import current_app
from celery.app.control import Inspect

inspector = Inspect(app=current_app)
print(inspector.active())  # Currently running tasks
print(inspector.scheduled())  # Scheduled tasks
print(inspector.registered())  # Available tasks
```

### Check Worker Logs

In PythonAnywhere:
1. Go to **Web** → **Log files**
2. Check:
   - **Server error log** (Celery errors)
   - **User error log** (Task errors)

### Monitor via Command Line

```bash
# SSH to PythonAnywhere
# Watch active tasks in real-time
celery -A alx_travel_app inspect active

# View registered tasks
celery -A alx_travel_app inspect registered

# Purge all pending tasks (careful!)
celery -A alx_travel_app purge
```

## Step 9: Configure Task Retries

Tasks can automatically retry on failure. Example in `settings.py`:

```python
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes hard limit
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes soft limit

# Retry policy
CELERY_TASK_AUTORETRY_FOR = (Exception,)
CELERY_TASK_MAX_RETRIES = 3
CELERY_TASK_DEFAULT_RETRY_DELAY = 60
```

## Step 10: Test Scheduled Tasks

### Test Email Reminders

```bash
python manage.py shell

# Trigger the reminder task manually
from listings.tasks import send_booking_reminders
result = send_booking_reminders.delay()
print(result.get(timeout=30))
```

### Test Payment Processing

```bash
# Simulate a payment callback
from listings.tasks import process_payment_callback
result = process_payment_callback.delay(1, 'success')
print(result.get(timeout=30))
```

## Troubleshooting

### Issue: "Connection refused" to RabbitMQ

**Solution:**
1. Check RabbitMQ is enabled in PythonAnywhere Account settings
2. Verify credentials in `.env` match RabbitMQ page
3. Test connection: `python manage.py shell`
   ```python
   from kombu import Connection
   conn = Connection(os.environ['CELERY_BROKER_URL'])
   print(conn)  # Should not raise exception
   ```

### Issue: Tasks not executing

**Solution:**
1. Check if worker is running:
   - PythonAnywhere → Tasks tab → Look for running worker
   - If not running, manually start: `celery -A alx_travel_app worker -l info`

2. Check task is queued:
   ```bash
   celery -A alx_travel_app inspect active
   ```

3. Check worker logs for errors

### Issue: "No module named 'kombu'"

**Solution:**
```bash
workon alx_travel_app
pip install kombu==5.3.4
```

### Issue: Tasks stuck in queue

**Solution:**
```bash
# Purge pending tasks
celery -A alx_travel_app purge

# Restart worker on PythonAnywhere
# Go to Tasks tab, stop and restart worker
```

### Issue: Duplicate periodic tasks

**Solution:**
1. Only run ONE Celery Beat instance
2. If duplicates exist, you may have multiple beat processes
3. Stop all beat processes: `pkill -f "celery.*beat"`

## Performance Tips

1. **Adjust worker concurrency:**
   ```bash
   celery -A alx_travel_app worker -l info --concurrency=4
   ```

2. **Set task time limits to prevent zombie tasks:**
   ```python
   CELERY_TASK_TIME_LIMIT = 1800  # 30 minutes
   ```

3. **Use task rate limiting to prevent overload:**
   ```bash
   celery -A alx_travel_app worker -l info --max-tasks-per-child=1000
   ```

4. **Monitor memory usage** (important on PythonAnywhere):
   ```bash
   celery -A alx_travel_app worker -l info --max-memory-per-child=200000  # 200MB
   ```

## Production Checklist

- [x] RabbitMQ enabled on PythonAnywhere
- [x] CELERY_BROKER_URL configured in `.env`
- [x] Celery worker running in background task
- [x] Celery Beat running (if using periodic tasks)
- [x] Email backend configured (SMTP)
- [x] Tasks tested manually
- [x] Error logging configured
- [x] Monitored logs for errors
- [x] Task retry policies configured
- [x] Performance monitoring enabled

## Useful Commands

```bash
# Start worker
celery -A alx_travel_app worker -l info

# Start beat
celery -A alx_travel_app beat -l info

# Inspect active tasks
celery -A alx_travel_app inspect active

# Inspect scheduled tasks
celery -A alx_travel_app inspect scheduled

# Purge queue (CAREFUL - deletes all pending tasks)
celery -A alx_travel_app purge

# Check worker stats
celery -A alx_travel_app inspect stats

# Restart workers
celery -A alx_travel_app control shutdown
```

## Cost Impact

- **Starter ($5/month)**: Includes RabbitMQ + 1 background task
- **Each additional background task**: +$2/month
- **Recommended setup**: 1 worker + 1 beat = ~$7/month total

## Next Steps

1. Enable RabbitMQ in PythonAnywhere
2. Configure `.env` with RabbitMQ credentials
3. Deploy Celery worker
4. Deploy Celery Beat (if using periodic tasks)
5. Test tasks via Django shell
6. Monitor logs for errors
7. Set up performance monitoring
