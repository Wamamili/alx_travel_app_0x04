import os
import django
from pathlib import Path

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
django.setup()

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
