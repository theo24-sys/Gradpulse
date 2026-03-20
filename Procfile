release: /opt/venv/bin/python manage.py migrate --noinput
web: /opt/venv/bin/gunicorn gradpulse.wsgi:application --log-file -
