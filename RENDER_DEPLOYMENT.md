# Render Deployment Guide for ALX Travel App

## Step 1: Prepare Your Local Environment

Ensure all files are committed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Step 2: Create Render Account & Connect GitHub

1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Grant Render access to your repositories
4. Select your `alx_travel_app_0x04` repository

## Step 3: Create a PostgreSQL Database on Render

1. In Render dashboard, click **New +** → **PostgreSQL**
2. Fill in details:
   - **Name**: `alx-travel-db`
   - **Region**: Select your region
   - **Database Name**: `alx_travel_db`
   - **User**: `postgres` (or custom)
3. Copy the internal and external connection strings
4. Note the `DATABASE_URL` (format: `postgresql://user:password@host:port/dbname`)

## Step 4: Create Redis Instance (Optional but Recommended for Celery)

1. Click **New +** → **Redis**
2. Fill in details:
   - **Name**: `alx-travel-redis`
   - **Region**: Same as database
3. Copy the Redis URL (format: `redis://:password@host:port`)

## Step 5: Deploy Web Service

1. In Render dashboard, click **New +** → **Web Service**
2. Select your GitHub repository
3. Fill in configuration:

   **Basic Settings:**
   - **Name**: `alx-travel-app`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn alx_travel_app.wsgi:application`

   **Environment Variables** (click "Add Environment Variable"):
   ```
   DEBUG=False
   SECRET_KEY=<generate-strong-key>
   DATABASE_URL=<from-postgres-step>
   ALLOWED_HOSTS=your-app.onrender.com,yourdomain.com
   CORS_ALLOWED_ORIGINS=https://your-app.onrender.com,https://yourdomain.com
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=<gmail-app-password>
   EMAIL_USE_TLS=True
   CELERY_BROKER_URL=<from-redis-step>
   CELERY_RESULT_BACKEND=<from-redis-step>
   CHAPA_SECRET_KEY=<your-chapa-key>
   ```

4. Click **Create Web Service**
5. Render will automatically deploy

## Step 6: Run Database Migrations

After deployment, run migrations via Render shell:

1. Go to your Web Service dashboard
2. Click **Shell** in the top menu
3. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

## Step 7: Deploy Celery Worker (Optional but Recommended)

For background tasks (email sending, payments):

1. In Render, click **New +** → **Background Worker**
2. Select your GitHub repository
3. Fill in configuration:

   **Basic Settings:**
   - **Name**: `alx-travel-worker`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `celery -A alx_travel_app worker -l info`

   **Environment Variables**: (Same as Web Service)
   - Copy all env vars from Web Service

4. Click **Create Background Worker**

## Step 8: Deploy Celery Beat (Optional - for scheduled tasks)

For scheduled/periodic tasks:

1. Click **New +** → **Background Worker**
2. Fill in configuration:

   **Basic Settings:**
   - **Name**: `alx-travel-beat`
   - **Start Command**: `celery -A alx_travel_app beat -l info`

   **Environment Variables**: (Same as above)

## Step 9: Verify Deployment

1. Visit your app: `https://your-app.onrender.com`
2. Check admin panel: `https://your-app.onrender.com/admin`
3. Check API docs: `https://your-app.onrender.com/swagger/`
4. Monitor logs in Render dashboard

## Step 10: Custom Domain (Optional)

1. In Web Service settings, go to **Custom Domain**
2. Add your domain (e.g., `api.yourdomain.com`)
3. Update DNS records with CNAME provided by Render

## Troubleshooting

### Issue: Database connection failed
- Check `DATABASE_URL` is correct
- Ensure database is active in Render
- Run migrations via Shell

### Issue: Static files not loading
- Run `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` and `STATIC_URL` in settings

### Issue: Celery tasks not running
- Check Redis connection string
- Verify worker logs in Render dashboard
- Ensure `CELERY_BROKER_URL` matches Redis instance

### Issue: Email not sending
- Verify Gmail app password (not account password)
- Enable "Less secure apps" if using regular Gmail
- Check email logs for errors

## Cost Estimate

- **Web Service**: Free tier (limited) or $7/month paid
- **PostgreSQL**: Free tier (500MB) or $15/month production
- **Redis**: Free tier (100MB) or $15/month production
- **Background Worker**: $12/month each

**Recommended for production**: ~$50-70/month minimum

## Environment Variables Summary

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Django debug mode | `False` |
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://...` |
| `ALLOWED_HOSTS` | Allowed domains | `app.onrender.com,yourdomain.com` |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `https://app.onrender.com` |
| `EMAIL_HOST_USER` | Email sender | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Email password | `app-password` |
| `CELERY_BROKER_URL` | Redis broker | `redis://:password@host:port` |
| `CHAPA_SECRET_KEY` | Chapa payment key | `cpseck_...` |

## Next Steps

1. Test all endpoints after deployment
2. Monitor error logs regularly
3. Set up uptime monitoring
4. Configure backups for database
5. Update DNS if using custom domain
