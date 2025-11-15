# PythonAnywhere Deployment Checklist

## Pre-Deployment (Local)

- [x] ✓ Cleaned up `settings.py` for PythonAnywhere (MySQL focus)
- [x] ✓ Updated `requirements.txt` (added MySQLdb)
- [x] ✓ Created `wsgi_pythonanywhere.py` template
- [ ] Test locally: `python manage.py runserver`
- [ ] Commit changes: `git add . && git commit -m "Prepare for PythonAnywhere deployment"`
- [ ] Push to GitHub: `git push origin main`

## PythonAnywhere Setup

### Account & Repository
- [ ] Create PythonAnywhere account (free or paid)
- [ ] Open Bash Console
- [ ] Clone repository: `git clone https://github.com/YOUR_USERNAME/alx_travel_app_0x04.git`
- [ ] Navigate: `cd alx_travel_app_0x04/alx_travel_app`

### Virtual Environment
- [ ] Create virtualenv: `mkvirtualenv --python=/usr/bin/python3.10 alx_travel_app`
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Verify: `python --version` (should be 3.10+)

### Database Setup
- [ ] Go to **Databases** tab
- [ ] Create MySQL database (free tier includes 1 DB)
- [ ] Note down credentials:
  - Database name: `username$alx_travel_db`
  - Host: `username.mysql.pythonanywhere-services.com`
  - Username: `username`
  - Password: `[your-mysql-password]`

### Environment Configuration
- [ ] Create/edit `.env` file in bash console:
```bash
nano ~/alx_travel_app_0x04/alx_travel_app/.env
```

Add:
```
DEBUG=False
SECRET_KEY=django-insecure-your-very-long-random-key-here
DB_ENGINE=django.db.backends.mysql
DB_NAME=username$alx_travel_db
DB_USER=username
DB_PASSWORD=your-mysql-password
DB_HOST=username.mysql.pythonanywhere-services.com
DB_PORT=3306
ALLOWED_HOSTS=username.pythonanywhere.com
CORS_ALLOWED_ORIGINS=https://username.pythonanywhere.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
EMAIL_USE_TLS=True
CHAPA_SECRET_KEY=your-chapa-secret-key
```

Save: `Ctrl+X` → `Y` → `Enter`

### Database Migrations
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
  - Username: `admin`
  - Email: `your@email.com`
  - Password: `[strong-password]`
- [ ] Collect static: `python manage.py collectstatic --noinput`

### Web App Configuration
- [ ] Go to **Web** tab → **Add a new web app**
- [ ] Choose **Manual configuration** → **Python 3.10**

### WSGI Configuration
- [ ] Click the WSGI configuration file link
- [ ] Replace entire content with (update USERNAME):
```python
import os
import sys
import django

path = '/home/USERNAME/alx_travel_app_0x04/alx_travel_app'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'alx_travel_app.settings'
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

- [ ] Save file

### Web App Settings
In **Web** tab for your app:

- [ ] **Python version**: Set to **Python 3.10**
- [ ] **Virtualenv**: `/home/USERNAME/.virtualenvs/alx_travel_app`
- [ ] **Working directory**: `/home/USERNAME/alx_travel_app_0x04/alx_travel_app`
- [ ] **WSGI configuration**: `/home/USERNAME/alx_travel_app_0x04/alx_travel_app/wsgi_pythonanywhere.py`

### Static & Media Files
- [ ] Add static file mapping:
  - **URL**: `/static/`
  - **Directory**: `/home/USERNAME/alx_travel_app_0x04/alx_travel_app/static`

- [ ] Add media file mapping:
  - **URL**: `/media/`
  - **Directory**: `/home/USERNAME/alx_travel_app_0x04/alx_travel_app/media`

### SSL Certificate
- [ ] In **Web** tab, scroll to **Security**
- [ ] Click **Force HTTPS**
- [ ] Wait 24 hours for Let's Encrypt certificate

### Reload & Deploy
- [ ] Click green **Reload** button at top of **Web** tab
- [ ] Wait for reload to complete

## Testing & Verification

### Basic Functionality
- [ ] Visit: `https://USERNAME.pythonanywhere.com/`
- [ ] Admin: `https://USERNAME.pythonanywhere.com/admin/`
- [ ] Login with superuser credentials
- [ ] API: `https://USERNAME.pythonanywhere.com/api/listings/`
- [ ] Docs: `https://USERNAME.pythonanywhere.com/swagger/`

### API Endpoints
- [ ] GET `/api/listings/` - should return empty list
- [ ] POST `/api/listings/` - create test listing
- [ ] GET `/api/bookings/` - should return empty list
- [ ] POST `/api/payments/initialize/` - test payment (requires booking)

### Admin Panel
- [ ] Create test listing via admin
- [ ] Create test booking
- [ ] Verify models are accessible

### Error Logs
- [ ] Check **Log files** in **Web** tab:
  - [ ] Server error log (for 500 errors)
  - [ ] User error log (for permission issues)
  - [ ] Access log (for request history)

## Updating Your App

To pull latest changes from GitHub:

```bash
cd ~/alx_travel_app_0x04/alx_travel_app
workon alx_travel_app  # Activate virtualenv
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then reload web app in PythonAnywhere dashboard.

## Troubleshooting

### Can't connect to database
- Bash command: `mysql -u USERNAME -p -h USERNAME.mysql.pythonanywhere-services.com alx_db`
- Check credentials in `.env` match database settings

### Import errors
- Activate virtualenv: `workon alx_travel_app`
- Check path in WSGI file
- Verify virtualenv is set correctly in Web tab

### Static files not loading
- Run: `python manage.py collectstatic --noinput`
- Check static path in Web tab matches `/home/USERNAME/alx_travel_app_0x04/alx_travel_app/static`

### 500 Internal Server Error
- Check error logs in Web tab
- Common issues:
  - Missing environment variables
  - Database connection failed
  - Import errors

### Email not sending
- Test from shell: `python manage.py shell`
- `>>> from django.core.mail import send_mail`
- `>>> send_mail('Test', 'Body', 'from@example.com', ['to@example.com'])`
- If no exception, email was sent

## Important Limitations (Free Tier)

❌ **No outbound internet** - Can't call Chapa API
❌ **No background tasks** - Celery won't work
❌ **No custom domain** - Limited to pythonanywhere.com
❌ **Limited resources** - Slower response times
❌ **100MB disk limit** - Monitor usage

## Upgrade Options

| Feature | Free | Starter | Professional |
|---------|------|---------|--------------|
| Cost | $0 | $5/mo | $20/mo |
| Storage | 512MB | 1GB | 2GB |
| Custom Domain | ❌ | ✅ | ✅ |
| Outbound Internet | ❌ | ✅ | ✅ |
| Background Tasks | ❌ | ❌ | ✅ |
| Email Access | ❌ | ✅ | ✅ |

**For Chapa payments: Need Starter ($5/mo) or higher**

## Next Steps

1. ✅ Deploy to free tier first
2. ✅ Test all endpoints
3. 📈 Monitor logs and performance
4. 💳 Upgrade to Starter tier for Chapa payments
5. 🔄 Set up automated git pulls for updates
6. 📊 Monitor error logs weekly

## Useful Commands

```bash
# Activate virtualenv
workon alx_travel_app

# Run Django shell
python manage.py shell

# Check migrations
python manage.py showmigrations

# Apply migrations
python manage.py migrate

# Create static files
python manage.py collectstatic --noinput

# View environment variables
cat ~/.env

# Pull latest code
git pull origin main
```
