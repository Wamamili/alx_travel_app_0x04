# PythonAnywhere Deployment Guide for ALX Travel App

## Step 1: Create PythonAnywhere Account

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free or paid account
3. Verify email and log in to your dashboard

## Step 2: Set Up Virtual Environment

1. Open **Bash Console** from the PythonAnywhere dashboard
2. Clone your GitHub repository:

```bash
git clone https://github.com/wamamili/alx_travel_app_0x04.git
cd alx_travel_app_0x04/alx_travel_app
```

3. Create and activate virtual environment:

```bash
mkvirtualenv --python=/usr/bin/python3.10 alx_travel_app
pip install --upgrade pip
pip install -r requirements.txt
```

4. Verify installation:

```bash
which python
python --version
```

## Step 3: Configure Database

### Option A: MySQL (Recommended for PythonAnywhere)

1. Go to **Databases** tab in PythonAnywhere
2. Create MySQL database:
   - **Database name**: `username$alx_travel_db`
   - **Username**: Your PythonAnywhere username
   - **Password**: Set a strong password
   - Save the connection details

3. Update `.env` file in your project:

```bash
nano ~/alx_travel_app_0x04/alx_travel_app/.env
```

Add/update:
```
DEBUG=False
SECRET_KEY=your-strong-secret-key-here
DB_ENGINE=django.db.backends.mysql
DB_NAME=username$alx_travel_db
DB_USER=username
DB_PASSWORD=your-mysql-password
DB_HOST=username.mysql.pythonanywhere-services.com
DB_PORT=3306
ALLOWED_HOSTS=username.pythonanywhere.com
CORS_ALLOWED_ORIGINS=https://username.pythonanywhere.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
EMAIL_USE_TLS=True
CHAPA_SECRET_KEY=your-chapa-secret-key
```

Press `Ctrl+X` → `Y` → `Enter` to save.

### Option B: PostgreSQL (More stable)

1. Install PostgreSQL adapter:

```bash
pip install psycopg2-binary
```

2. Set `.env`:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=username_alx_db
DB_USER=username
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

## Step 4: Run Database Migrations

From your virtual environment bash console:

```bash
cd ~/alx_travel_app_0x04/alx_travel_app
python manage.py migrate
python manage.py createsuperuser
```

Follow the prompts to create admin account.

## Step 5: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

Note the output path (usually `/home/username/alx_travel_app_0x04/alx_travel_app/static/`)

## Step 6: Create WSGI Configuration

1. Go to **Web** tab in PythonAnywhere
2. Click **Add a new web app**
3. Select **Manual Configuration** → **Python 3.10**
4. Click the WSGI configuration file link (opens editor)
5. Replace content with:

```python
import os
import sys
import django
from pathlib import Path

# Add project to path
path = '/home/username/alx_travel_app_0x04/alx_travel_app'
if path not in sys.path:
    sys.path.append(path)

# Set Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'alx_travel_app.settings'

# Setup Django
django.setup()

# Get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Replace `username` with your PythonAnywhere username.

6. Save file

## Step 7: Configure Web App Settings

In PythonAnywhere **Web** tab for your app:

### Python version
- Set to **Python 3.10** (or your preferred version)

### Virtualenv
- Set virtualenv path: `/home/username/.virtualenvs/alx_travel_app`

### Source code
- Working directory: `/home/username/alx_travel_app_0x04/alx_travel_app`

### Static files
1. Add static mapping:
   - **URL**: `/static/`
   - **Directory**: `/home/username/alx_travel_app_0x04/alx_travel_app/static`

2. Add media mapping:
   - **URL**: `/media/`
   - **Directory**: `/home/username/alx_travel_app_0x04/alx_travel_app/media`

### WSGI configuration
- Point to the WSGI file created in Step 6

## Step 8: Enable HTTPS (SSL Certificate)

1. In **Web** tab, scroll to "Security"
2. Click **Force HTTPS**
3. Wait 24 hours for Let's Encrypt certificate to activate

## Step 9: Reload Web App

1. Click the green **Reload** button at the top of **Web** tab
2. Wait for reload to complete
3. Visit `https://username.pythonanywhere.com`

## Step 10: Verify Deployment

- [ ] Admin panel: `https://username.pythonanywhere.com/admin/`
- [ ] API endpoint: `https://username.pythonanywhere.com/api/listings/`
- [ ] Swagger docs: `https://username.pythonanywhere.com/swagger/`
- [ ] Create test listing via admin
- [ ] Test booking creation via API

## Step 11: Configure Email (Background Tasks)

### Option 1: Django's Built-in Email (Synchronous)
- Works with free tier
- Emails send during request (slower)
- Already configured in `.env`

### Option 2: Celery + Redis (Requires Paid Account)
- Enables background task processing
- Needs Redis instance (paid feature)
- More complex setup

For free tier, use **Option 1** (built-in email).

## Step 12: Set Up Git Pulls for Updates

To update your app with latest code:

```bash
cd ~/alx_travel_app_0x04/alx_travel_app
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then reload the web app in PythonAnywhere dashboard.

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"

**Solution:**
```bash
workon alx_travel_app  # Activate virtualenv
pip install -r requirements.txt
```

### Issue: Static files not loading

**Solution:**
```bash
python manage.py collectstatic --noinput
# Verify path matches in Web tab settings
```

### Issue: Database connection refused

**Solution:**
- Check `.env` file has correct credentials
- Verify database is created in PythonAnywhere
- Restart MySQL service (if using MySQL)
- Test connection from bash: `mysql -u username -p -h username.mysql.pythonanywhere-services.com alx_db`

### Issue: Migrations not applied

**Solution:**
```bash
python manage.py showmigrations
python manage.py migrate --run-syncdb
```

### Issue: 500 Error - Check error logs

**Solution:**
1. View logs in PythonAnywhere **Web** tab → **Log files**
2. Check:
   - Server error log
   - User error log
   - Access log

### Issue: Email not sending

**Solution:**
```bash
# Test from Django shell
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Hello', 'noreply@yourdomain.com', ['your@email.com'])
# Check output - no exceptions = success
```

## Important Notes

- **PythonAnywhere Free Tier Limitations:**
  - Limited to pythonanywhere.com subdomain
  - No outbound internet (can't call external APIs like Chapa)
  - No background task scheduling (Celery)
  - Slower response times
  - CPU restrictions

- **Upgrade to Paid for:**
  - Custom domain
  - Outbound internet access (for Chapa payments)
  - Background tasks (Celery + Redis)
  - Better performance
  - Email configuration

## Cost

- **Free Tier**: $0 (limited)
- **Starter**: $5/month (custom domain, outbound internet)
- **Professional**: $20/month (better resources)

## Next Steps

1. Deploy to PythonAnywhere free tier first
2. Test all features
3. Upgrade to Starter tier when ready for custom domain + Chapa payments
4. Monitor error logs and performance
5. Set up regular backups of database

## Useful Links

- PythonAnywhere Docs: https://help.pythonanywhere.com
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- MySQL on PythonAnywhere: https://help.pythonanywhere.com/pages/UsingMySQL/
- Custom Domain: https://help.pythonanywhere.com/pages/PaidAccounts/
