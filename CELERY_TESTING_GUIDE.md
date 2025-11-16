# Background Task Testing & Verification Guide

## Overview

This guide provides step-by-step instructions to verify that all background tasks (Celery) work correctly in your live environment.

## Part 1: Manual Task Execution (Local Testing)

### Test 1: Debug Task

```bash
python manage.py shell

# Import and run debug task
from listings.tasks import debug_task
task = debug_task.delay()
print(f"Task ID: {task.id}")
print(f"Task Status: {task.status}")
print(f"Task Result: {task.get(timeout=10)}")
```

**Expected Output:**
```
Task ID: abc123def456...
Task Status: SUCCESS
Task Result: {'status': 'success', 'message': 'Debug task ran'}
```

### Test 2: Send Email Task

```bash
# In Django shell
from listings.tasks import send_booking_confirmation_email

# Trigger the task
task = send_booking_confirmation_email.delay(
    booking_id=1,
    customer_email='test@example.com',
    customer_name='John Doe',
    listing_title='Luxury Beach Villa',
    check_in='2025-11-20',
    check_out='2025-11-25'
)

print(f"Task ID: {task.id}")
print(f"Status: {task.status}")

# Wait for result
result = task.get(timeout=30)
print(f"Result: {result}")
```

**Expected Output:**
```
Task ID: xyz789...
Status: SUCCESS
Result: {'status': 'success', 'booking_id': 1, 'email_sent': 1}
```

### Test 3: Booking Reminders

```bash
from listings.tasks import send_booking_reminders

task = send_booking_reminders.delay()
result = task.get(timeout=30)
print(f"Reminders sent: {result}")
```

**Expected Output:**
```
{'status': 'success', 'reminders_sent': 0}  # 0 if no upcoming bookings
```

## Part 2: Real-World Workflow Testing

### Scenario 1: New Booking Triggers Email

**Steps:**
1. Create a booking via API:

```bash
curl -X POST https://username.pythonanywhere.com/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "listing": 1,
    "customer_name": "Jane Smith",
    "customer_email": "jane@example.com",
    "check_in": "2025-12-01",
    "check_out": "2025-12-05",
    "total_price": "450.00"
  }'
```

2. Check email received at `jane@example.com`

3. Verify in logs:
   ```bash
   # In bash console
   tail -f ~/alx_travel_app_0x04/alx_travel_app/logs/celery.log
   ```

**Expected Result:**
- Email arrives within 10-30 seconds
- Log shows: `Booking confirmation email sent for booking X`

### Scenario 2: Payment Processing

```bash
from listings.tasks import process_payment_callback

# Simulate successful payment
task = process_payment_callback.delay(payment_id=1, chapa_status='success')
result = task.get(timeout=30)
print(result)

# Verify payment status in admin
# Admin → Payments → Check status changed to 'Completed'
```

### Scenario 3: Periodic Task (Booking Reminders)

The `send_booking_reminders` task runs **every hour** (configured in settings).

**To test manually:**
```bash
# Create a booking with tomorrow's check-in date
# Then run:
from listings.tasks import send_booking_reminders
task = send_booking_reminders.delay()
print(task.get(timeout=30))

# Expected: reminder email sent to customer
```

## Part 3: Monitor Celery Workers

### Check Active Tasks

```bash
# In bash console
python manage.py shell

from celery import current_app
from celery.app.control import Inspect

inspector = Inspect(app=current_app)

# View all active tasks
print(inspector.active())

# View scheduled tasks
print(inspector.scheduled())

# View registered tasks
print(inspector.registered())

# View worker stats
print(inspector.stats())
```

**Example Output:**
```python
{
  'celery@hostname': {
    'pool': {'implementation': 'solo', 'max-concurrency': 1},
    'total': 5,
    'clock': '2025-11-15T10:30:45.123456',
    'rusage': {...}
  }
}
```

### Monitor via Command Line

```bash
# Watch tasks in real-time
watch -n 1 'celery -A alx_travel_app inspect active'

# Get worker pool stats
celery -A alx_travel_app inspect stats

# Get active task details
celery -A alx_travel_app inspect active
```

### PythonAnywhere Task Monitoring

1. Go to **Web** tab → **Log files**
2. Check:
   - **Error log** - Celery errors
   - **Access log** - Request logs
3. Download logs for detailed analysis

## Part 4: Automated Testing

### Create Django Management Command for Testing

Create `listings/management/commands/test_celery.py`:

```python
from django.core.management.base import BaseCommand
from listings.tasks import (
    debug_task,
    send_booking_confirmation_email,
    send_booking_reminders,
    cleanup_old_bookings,
)


class Command(BaseCommand):
    help = 'Test all Celery tasks'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Celery tests...'))

        # Test 1: Debug Task
        self.stdout.write('Test 1: Debug Task')
        try:
            result = debug_task.delay()
            output = result.get(timeout=30)
            self.stdout.write(self.style.SUCCESS(f'✓ Debug task: {output}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Debug task failed: {e}'))

        # Test 2: Email Task
        self.stdout.write('Test 2: Send Email Task')
        try:
            result = send_booking_confirmation_email.delay(
                1, 'test@example.com', 'Test User',
                'Test Villa', '2025-11-20', '2025-11-25'
            )
            output = result.get(timeout=30)
            self.stdout.write(self.style.SUCCESS(f'✓ Email task: {output}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Email task failed: {e}'))

        # Test 3: Booking Reminders
        self.stdout.write('Test 3: Booking Reminders')
        try:
            result = send_booking_reminders.delay()
            output = result.get(timeout=30)
            self.stdout.write(self.style.SUCCESS(f'✓ Reminders task: {output}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Reminders task failed: {e}'))

        # Test 4: Cleanup
        self.stdout.write('Test 4: Cleanup Old Bookings')
        try:
            result = cleanup_old_bookings.delay()
            output = result.get(timeout=30)
            self.stdout.write(self.style.SUCCESS(f'✓ Cleanup task: {output}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Cleanup task failed: {e}'))

        self.stdout.write(self.style.SUCCESS('\nAll tests completed!'))
```

**Run tests:**
```bash
python manage.py test_celery
```

## Part 5: Error Scenarios & Debugging

### Scenario: Task Fails to Connect to RabbitMQ

**Error Message:**
```
[ERROR/MainProcess] Error connecting to amqp://...
```

**Fix:**
1. Verify RabbitMQ credentials in `.env`
2. Test connection manually:
   ```bash
   python manage.py shell
   >>> from kombu import Connection
   >>> import os
   >>> conn = Connection(os.environ['CELERY_BROKER_URL'])
   >>> print(conn.connect())
   ```

### Scenario: Task Timeout

**Error Message:**
```
Task ... TimeLimitExceeded
```

**Fix:**
1. Increase time limit in settings:
   ```python
   CELERY_TASK_TIME_LIMIT = 3600  # 1 hour
   ```
2. Optimize task code to run faster
3. Split task into smaller subtasks

### Scenario: Duplicate Emails Sent

**Cause:** Celery task retried multiple times

**Fix:**
1. Check retry configuration
2. Implement task idempotency (use unique task IDs)
3. Monitor for retry errors

### Scenario: Task Never Executes

**Possible Causes:**
1. Worker not running
2. Task not registered
3. Task queue full

**Debug:**
```bash
# Check if worker is running
celery -A alx_travel_app inspect active

# List all registered tasks
celery -A alx_travel_app inspect registered

# Check queue
python manage.py shell
>>> from kombu import Connection
>>> conn = Connection(os.environ['CELERY_BROKER_URL'])
>>> conn.default_channel.queue_declare('celery')
```

## Part 6: Performance Testing

### Load Test Email Tasks

```python
# In Django shell
from listings.tasks import send_booking_confirmation_email
import time

# Send 100 emails asynchronously
start = time.time()
for i in range(100):
    send_booking_confirmation_email.delay(
        i, f'user{i}@example.com', f'User {i}',
        'Villa', '2025-11-20', '2025-11-25'
    )

print(f"Queued 100 tasks in {time.time() - start:.2f}s")

# Monitor queue processing
time.sleep(5)
from celery import current_app
from celery.app.control import Inspect
inspector = Inspect(app=current_app)
print(f"Active: {inspector.active()}")
print(f"Reserved: {inspector.reserved()}")
```

### Monitor Memory Usage

```bash
# Check worker memory
ps aux | grep celery

# Monitor in real-time
watch -n 1 'ps aux | grep celery'
```

## Part 7: Logging & Monitoring

### Configure Task Logging

In `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'celery.log'),
        },
    },
    'loggers': {
        'listings.tasks': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### View Logs

```bash
# Real-time logs
tail -f ~/alx_travel_app_0x04/alx_travel_app/logs/celery.log

# Search for errors
grep ERROR ~/alx_travel_app_0x04/alx_travel_app/logs/celery.log

# Count task executions
grep "successfully" ~/alx_travel_app_0x04/alx_travel_app/logs/celery.log | wc -l
```

## Part 8: Production Verification Checklist

- [ ] Debug task executes successfully
- [ ] Email task sends emails within 30 seconds
- [ ] Booking reminder task runs hourly
- [ ] Payment callback task processes correctly
- [ ] Worker shows as active in Celery inspect
- [ ] No timeout errors in logs
- [ ] Memory usage stable (< 500MB)
- [ ] No duplicate tasks
- [ ] Retry mechanism works on failure
- [ ] Monitoring alerts configured
- [ ] Logs rotated regularly
- [ ] Dashboard shows task metrics

## Performance Metrics

| Metric | Target | Your Value |
|--------|--------|-----------|
| Avg Email Send Time | < 5s | |
| Task Queue Size | < 100 | |
| Worker Memory | < 300MB | |
| Email Success Rate | > 99% | |
| Task Retry Rate | < 1% | |

## Support & Troubleshooting

**Common Issues:**

1. **Worker crashed**
   - Check PythonAnywhere background tasks
   - Restart worker manually

2. **RabbitMQ disconnected**
   - Verify credentials
   - Check network connectivity
   - Restart RabbitMQ (via PythonAnywhere)

3. **Tasks stuck in queue**
   - Purge queue: `celery -A alx_travel_app purge`
   - Restart worker

4. **Email not sent**
   - Check EMAIL_BACKEND is SMTP
   - Verify Gmail app password
   - Check firewall/network access

## Next Steps

1. ✅ Deploy Celery worker to PythonAnywhere
2. ✅ Run manual tests
3. ✅ Monitor logs for errors
4. ✅ Test real workflows (create booking → email)
5. ✅ Set up automated performance monitoring
6. ✅ Configure alerts for task failures
7. ✅ Document any custom tasks
