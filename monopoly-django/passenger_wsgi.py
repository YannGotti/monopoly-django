import os, sys
sys.path.insert(0, '/var/www/u1625777/data/www/cyphergo.ru/monopoly')
sys.path.insert(1, '/var/www/u1625777/data/djangoenv/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'monopoly.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()