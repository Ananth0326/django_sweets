# vercel_app.py
import os
from django.core.wsgi import get_wsgi_application

# FIX: Changed from "sweetspot.settings" to "settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = get_wsgi_application()
