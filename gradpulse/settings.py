"""
GradPulse Django Settings
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-gradpulse-change-in-production-xyz-123-abc'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # Jazzmin must be before django.contrib.admin
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
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
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'gradpulse.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/auth/login/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

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
