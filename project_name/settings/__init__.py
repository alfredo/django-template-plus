# Django settings for {{ project_name }} project.
import datetime
import os
import dj_database_url

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
# settings is one directory up now
here = lambda *x: os.path.join(PROJECT_ROOT, '..', *x)
env = lambda x: os.getenv(x)


# Heroku DB requirements
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
# DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Make this unique, and don't share it with anybody.
SECRET_KEY = env('SECRET_KEY')


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = here('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = here('..', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    here('assets'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#    '{{ project_name }}.common.middleware.BasicAuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
#    '{{ project_name }}.common.context_processors.settings_available',
)

ROOT_URLCONF = '{{ project_name }}.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

TEMPLATE_DIRS = (
    here('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'gunicorn',
    'compressor',
    '{{ project_name }}.common',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'heroku': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '{{ project_name }}.common': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}


EMAIL_SUBJECT_PREFIX = '[{{ project_name }}] '

SEND_BROKEN_LINK_EMAILS = True

ALLOWED_HOSTS = [
    '{{ project_url }}',
    '{{ heroku_app }}.herokuapp.com',
]

# Static assets handling
STATICFILES_STORAGE = '{{ project_name }}.common.storage.StaticS3Storage'
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
COMPRESS_ROOT = here('assets')
AWS_IS_GZIPPED = True

# Compressed files are required remotely and locally
COMPRESS_STORAGE = '{{ project_name }}.common.storage.CachedS3BotoStorage'

# Expire headers for the uploaded assets
expire_date = datetime.date.today() + datetime.timedelta(days=365)
expire_seconds = 30 * 24 * 60 * 60

AWS_S3_CUSTOM_DOMAIN = 'static.{{ project_url }}.s3.amazonaws.com'
AWS_S3_SECURE_URLS = False

AWS_HEADERS = {
    'Expires': expire_date.strftime('%a, %d %b %Y 00:00:00 GMT'),
    'Cache-Control': 'max-age=%s' % expire_seconds,
}

# Storage details
DEFAULT_FILE_STORAGE = '{{ project_name }}.common.storage.MediaS3Storage'

# Static assets
# AWS credentials
AWS_ACCESS_KEY_ID = env('AWS_KEY')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET')
AWS_STORAGE_BUCKET_NAME = 'static.{{ project_url }}'
STATIC_FILES_VERSION = 'v0'
COMPRESS_OFFLINE_MANIFEST = 'manifest.%s.json' % STATIC_FILES_VERSION

STATIC_URL = 'http://%s/static/%s/' % (AWS_S3_CUSTOM_DOMAIN,
                                       STATIC_FILES_VERSION)
