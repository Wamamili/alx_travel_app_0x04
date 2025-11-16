# Render Deployment Guide for ALX Travel App (copied)

See `alx_travel_app/RENDER_DEPLOYMENT.md` for the original, detailed step-by-step guide. This file is a lightweight pointer for deploying on Render.

Quick outline:

- Create a Render account and connect this GitHub repo
- Create a PostgreSQL database service and (optionally) a Redis service
- Create a Web Service with build command `pip install -r requirements.txt` and start command `gunicorn alx_travel_app.wsgi:application`
- Add environment variables: `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, `CELERY_BROKER_URL`, etc.
- Create Background Worker service(s) for Celery workers and Beat if needed
- Run `python manage.py migrate` from the Render shell and `python manage.py collectstatic --noinput`

For the full deploy guide, open `alx_travel_app/RENDER_DEPLOYMENT.md`.
