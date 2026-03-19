release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn gradpulse.wsgi:application --log-file -
