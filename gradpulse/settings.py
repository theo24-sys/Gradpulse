"""
GradPulse Django Settings
"""
import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY', default='django-insecure-gradpulse-change-in-production-xyz-123-abc')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
GOOGLE_API_KEY = env('GOOGLE_API_KEY', default='')

INSTALLED_APPS = [
    # Jazzmin must be before django.contrib.admin
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # required by allauth

    # Third-party Production Stack
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_filters',
    'django_celery_results',
    'storages',
    'anymail',
    'django_celery_beat',
    
    'crispy_forms',
    'crispy_bootstrap5',

    # GradPulse apps
    'accounts',
    'opportunities',
    'grades',
    'credentials',
    'events',
    'networking',
    'notifications',
    'scraping',
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'gradpulse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.notification_count',
                'accounts.context_processors.live_counts',
            ],
        },
    },
]

WSGI_APPLICATION = 'gradpulse.wsgi.application'

DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static and Media Config
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

WHITENOISE_MANIFEST_STRICT = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/auth/login/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ─── Django AllAuth ───────────────────────────────────────────────────────────
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# ─── REST Framework & Swagger ─────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'GradPulse API',
    'DESCRIPTION': 'GradPulse Core API matching university students to employers',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# ─── CORS & CSRF ──────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = DEBUG
if not DEBUG:
    CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
        'http://localhost:3000',
        'https://gradpulse.up.railway.app',
        'https://gradpulse.co.ke',
    ])
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
    CORS_ALLOW_HEADERS = ['accept', 'accept-encoding', 'authorization', 'content-type', 'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with']

CSRF_TRUSTED_ORIGINS = [
    'https://gradpulse.up.railway.app',
    'https://gradpulse.co.ke',
    'http://localhost:3000',
]

# ─── Password Hashers (Bcrypt) ────────────────────────────────────────────────
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# ─── Celery & Celery Results ──────────────────────────────────────────────────
CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'scrape-opportunities-daily': {
        'task': 'scraping.tasks.run_opportunity_scrapers',
        'schedule': crontab(hour=6, minute=0), # 6am Africa/Nairobi (server should be in EAT or env TZ set)
    },
    'scrape-events-twice-daily': {
        'task': 'scraping.tasks.run_event_scrapers',
        'schedule': crontab(hour='6,18', minute=0), # 6am and 6pm
    },
    'scrape-credentials-weekly': {
        'task': 'scraping.tasks.run_credential_scrapers',
        'schedule': crontab(hour=2, minute=0, day_of_week='monday'),
    },
    'scrape-qualifications-weekly': {
        'task': 'scraping.tasks.run_qualification_scrapers',
        'schedule': crontab(hour=3, minute=0, day_of_week='monday'),
    },
    'scrape-youth-programs-weekly': {
        'task': 'scraping.tasks.run_youth_program_scrapers',
        'schedule': crontab(hour=4, minute=0, day_of_week='monday'),
    },
    'scrape-simulations-weekly': {
        'task': 'scraping.tasks.run_simulation_scrapers',
        'schedule': crontab(hour=5, minute=0, day_of_week='monday'),
    },
    'scrape-all-full-weekly': {
        'task': 'scraping.tasks.run_all_scrapers',
        'schedule': crontab(hour=1, minute=0, day_of_week='sunday'),
    },
}

# ─── Email (Resend via Anymail) ───────────────────────────────────────────────
if env('RESEND_API_KEY', default=''):
    ANYMAIL = {
        "RESEND_API_KEY": env('RESEND_API_KEY'),
    }
    EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='hello@gradpulse.com')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ─── File Storage (Cloudflare R2 / AWS S3 / WhiteNoise) ────────────────────────
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

if env('AWS_ACCESS_KEY_ID', default=''):
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN', default=None)
    AWS_QUERYSTRING_AUTH = False  # Make media links public
    
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage"
    }
    
    if AWS_S3_CUSTOM_DOMAIN:
        # Strip https:// or http:// if user accidentally added it to the env var
        clean_domain = AWS_S3_CUSTOM_DOMAIN.replace('https://', '').replace('http://', '').rstrip('/')
        MEDIA_URL = f'https://{clean_domain}/'
    else:
        MEDIA_URL = f'{AWS_S3_ENDPOINT_URL.rstrip("/")}/{AWS_STORAGE_BUCKET_NAME}/'

# ─── Jazzmin Admin Settings ───────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "GradPulse Admin",
    "site_header": "GradPulse",
    "site_brand": "🎓 GradPulse",
    "site_logo": None,
    "login_logo": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Welcome to GradPulse Admin Panel",
    "copyright": "Ridge Technologies © 2026",
    "search_model": ["accounts.CustomUser", "opportunities.Opportunity"],
    "user_avatar": "profile_photo",

    # Top navigation
    "topmenu_links": [
        {"name": "Home", "url": "/", "new_window": True},
        {"name": "Campus Portal", "url": "/campus/dashboard/", "new_window": True},
        {"name": "Corporate Portal", "url": "/corporate/dashboard/", "new_window": True},
        {"model": "accounts.CustomUser"},
    ],

    # Side navigation
    "usermenu_links": [
        {"model": "accounts.CustomUser"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,

    "hide_apps": [],
    "hide_models": [],

    "order_with_respect_to": [
        "accounts",
        "opportunities",
        "grades",
        "credentials",
        "events",
        "networking",
        "notifications",
    ],

    "icons": {
        "auth": "fas fa-users-cog",
        "accounts.CustomUser": "fas fa-user-graduate",
        "opportunities.Opportunity": "fas fa-briefcase",
        "opportunities.Application": "fas fa-file-alt",
        "grades.Grade": "fas fa-chart-line",
        "credentials.Credential": "fas fa-certificate",
        "credentials.Enrollment": "fas fa-book-open",
        "events.Event": "fas fa-calendar-alt",
        "events.RSVP": "fas fa-ticket-alt",
        "networking.Connection": "fas fa-handshake",
        "networking.Collaboration": "fas fa-people-arrows",
        "notifications.Notification": "fas fa-bell",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-teal",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "slate",
    "dark_mode_theme": "slate",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-outline-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

# reCAPTCHA Configuration
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY', default='')
SILENT_RECAPTCHA_V3 = True
