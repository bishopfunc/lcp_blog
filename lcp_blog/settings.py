from django.contrib import messages
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': '',
        'HOST': 'host',
        'PORT': '',
    }
}
try:
    from .local_settings import *
except ImportError:
    pass

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts.apps.PostsConfig',
    'mdeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # ??

X_FRAME_OPTIONS = 'SAMEORIGIN' #3.0以上のみ

ROOT_URLCONF = 'lcp_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'posts.context.related',
            ],
        },
    },
]

WSGI_APPLICATION = 'lcp_blog.wsgi.application'

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

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# static set
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
	
MDEDITOR_CONFIGS = {
    'default': {
        'width': '100% ',  # Custom edit box width
        'height': 600,  # Custom edit box height
        'language': 'en',
        'lineWrapping': True
    }
}
MESSAGE_TAGS = {
    messages.INFO: 'alert alert-info',
    messages.SUCCESS: 'alert alert-success',
    messages.WARNING: 'alert alert-warning',
    messages.ERROR: 'alert alert-danger',
}

# if not DEBUG:
SECRET_KEY = os.environ['MY_SECRET_KEY']
import django_heroku #追加
django_heroku.settings(locals()) #追加



db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)

