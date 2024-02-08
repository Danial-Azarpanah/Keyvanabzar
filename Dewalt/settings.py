import os.path
from os import path
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = False

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ["www.keyvanabzar.com", "keyvanabzar.com"]
CSRF_TRUSTED_ORIGINS = ['https://*.dewalt-land.com']


INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    "home.apps.HomeConfig",
    "accounts.apps.AccountsConfig",
    "product.apps.ProductConfig",
    "payment.apps.PaymentConfig",
    "blog.apps.BlogConfig",

    # Libraries
    "ckeditor",
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

ROOT_URLCONF = 'Dewalt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'context-processors.context-processors.category_list',
                'context-processors.context-processors.cart_info',
                'context-processors.context-processors.info',
                'context-processors.context-processors.favorites',
            ],
        },
    },
]

WSGI_APPLICATION = 'Dewalt.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "dewaltla_dewalt-land",
        "USER": "dewaltla_admin",
        "PASSWORD": "daniel8203",
        "HOST": "127.0.0.1",
        "PORT": "3306"
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    path.join(BASE_DIR, "assets")
]
STATIC_ROOT = "/home/dewaltla/public_html/static"
# STATIC_ROOT = path.join(BASE_DIR, "static")

MEDIA_URL = 'media/'
MEDIA_ROOT = "/home/dewaltla/public_html/media"
# MEDIA_ROOT = path.join(BASE_DIR, "media")
TEMPLATE_CONTEXT_PROCESSORS = "django.contrib.messages.context_processors.messages"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "accounts.User"

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
