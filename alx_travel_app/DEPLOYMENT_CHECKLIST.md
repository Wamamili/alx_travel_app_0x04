# ALX Travel App - Render Deployment Checklist

## Pre-Deployment (Local)

- [x] ✓ Updated `requirements.txt` with pinned versions
- [x] ✓ Created `Procfile` with web, worker, and beat processes
- [x] ✓ Created `runtime.txt` with Python version
- [x] ✓ Created `.env.example` with all environment variables
- [x] ✓ Updated `settings.py` to support Render's `DATABASE_URL`
- [ ] Test locally: `python manage.py runserver`
- [ ] Commit all changes: `git add . && git commit -m "Ready for Render deployment"`
- [ ] Push to GitHub: `git push origin main`

## Render Setup

### Database
- [ ] Create PostgreSQL instance on Render
  - [ ] Database name: `alx_travel_db`
  - [ ] Save `DATABASE_URL`
  - [ ] Note the internal connection string

### Redis (Optional but Recommended)
- [ ] Create Redis instance on Render
  - [ ] Instance name: `alx-travel-redis`
  - [ ] Save Redis connection URL

### Web Service
- [ ] Create Web Service on Render
  - [ ] Connect GitHub repository
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `gunicorn alx_travel_app.wsgi:application`

### Environment Variables (Web Service)
Add these in Render dashboard:
```
DEBUG=False
SECRET_KEY=<generate-with-Django-secret-key-generator>
DATABASE_URL=<from-PostgreSQL-instance>
ALLOWED_HOSTS=your-app.onrender.com,yourdomain.com
CORS_ALLOWED_ORIGINS=https://your-app.onrender.com,https://yourdomain.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<gmail-app-specific-password>
EMAIL_USE_TLS=True
CELERY_BROKER_URL=<from-Redis-instance>
CELERY_RESULT_BACKEND=<from-Redis-instance>
CHAPA_SECRET_KEY=<your-chapa-secret-key>
```

- [ ] Set all environment variables
- [ ] Deploy Web Service

### Post-Deployment
- [ ] Wait for deployment to complete (check logs)
- [ ] Open Render shell for Web Service
- [ ] Run: `python manage.py migrate`
- [ ] Run: `python manage.py createsuperuser`
- [ ] Test API: `https://your-app.onrender.com/api/listings/`
- [ ] Test Admin: `https://your-app.onrender.com/admin/`
- [ ] Test Swagger: `https://your-app.onrender.com/swagger/`

### Background Worker (Optional)
- [ ] Create Background Worker on Render
  - [ ] Start Command: `celery -A alx_travel_app worker -l info`
  - [ ] Add same environment variables as Web Service

### Celery Beat (Optional - for scheduled tasks)
- [ ] Create Background Worker on Render
  - [ ] Name: `alx-travel-beat`
  - [ ] Start Command: `celery -A alx_travel_app beat -l info`
  - [ ] Add same environment variables

## Testing

### API Endpoints
- [ ] `GET /api/listings/` - List all listings
- [ ] `POST /api/listings/` - Create listing
- [ ] `GET /api/bookings/` - List all bookings
- [ ] `POST /api/bookings/` - Create booking
- [ ] `POST /api/payments/initialize/` - Initialize payment
- [ ] `GET /api/payments/verify/?tx_ref=...` - Verify payment

### Admin Panel
- [ ] Login at `/admin/`
- [ ] Verify all models are accessible
- [ ] Test creating a test listing

### Email (if configured)
- [ ] Create a booking and verify confirmation email
- [ ] Check Django logs for email sending status

### Celery Tasks (if worker deployed)
- [ ] Check worker logs: should see `Ready to accept tasks`
- [ ] Trigger a task and verify it completes

## Monitoring

- [ ] Set up Render logs monitoring
- [ ] Monitor error logs regularly
- [ ] Test uptime (optional: add uptime monitoring service)
- [ ] Monitor database connections
- [ ] Monitor Redis/Celery queue

## Custom Domain (Optional)

- [ ] Add custom domain in Render Web Service settings
- [ ] Update DNS CNAME record
- [ ] Verify HTTPS certificate (auto-provisioned)
- [ ] Update `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`

## Troubleshooting Commands

If you encounter issues, use these in Render Shell:

```bash
# Check migrations status
python manage.py showmigrations

# Re-run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Check Django settings
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES)
>>> print(settings.CELERY_BROKER_URL)

# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Hello', 'from@example.com', ['to@example.com'])

# View environment variables
import os
print(os.environ)
```

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] `SECRET_KEY` is strong and not exposed
- [ ] `ALLOWED_HOSTS` includes only your domain
- [ ] `CORS_ALLOW_ALL_ORIGINS=False` (use specific origins)
- [ ] Email credentials are app-specific passwords, not account passwords
- [ ] Database credentials are stored only in Render environment
- [ ] Redis connection string is secure
- [ ] Chapa secret key is stored securely

## Estimated Timeline

- Setup: 10-15 minutes
- Database creation: 2-3 minutes
- First deployment: 3-5 minutes
- Migrations + testing: 5-10 minutes
- **Total: ~20-30 minutes**

## Support Resources

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Celery & Render: https://render.com/docs/deploy-celery
- Chapa Docs: https://docs.chapa.co
