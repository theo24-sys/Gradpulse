release: /opt/venv/bin/python manage.py migrate --noinput
web: /opt/venv/bin/gunicorn gradpulse.wsgi:application --log-file -
worker: /opt/venv/bin/celery -A gradpulse worker -l info
beat: /opt/venv/bin/celery -A gradpulse beat -l info
