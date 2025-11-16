import os
import sys
import django
from pathlib import Path

# Add project to Python path
path = '/home/USERNAME/alx_travel_app_0x04/alx_travel_app'
if path not in sys.path:
    sys.path.append(path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'alx_travel_app.settings'

# Setup Django
django.setup()

# Import and return WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
