# -*- coding: utf-8 -*-
# Django settings for real project.

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    ('qq6ka', 'abukhvalov@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
	'USER': 'root',
	'PASSWORD': '',
	'HOST': 'localhost',
        'NAME': 'test'
    }
}


EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Yakutsk'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False
DECIMAL_SEPARATOR=","
TIMEOUT=3
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = 'C:/fat/site_media'
MEDIA_ROOT = '/home/root2/mptt/bc/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = '/home/root2/mptt/bc/static/'


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '12f_*9t-6x9$v47#c(*9iqxw0v*b7js3t&oc8uu89q*+pz2*v9'
SITE_ID=1

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

CACHE_MIDDLEWARE_SECONDS = 0

DATE_INPUT_FORMATS=(
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
	'%d.%m.%Y',
)

# List of callables that know how to import templates from various sources.
if DEBUG:
    TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',      
    ]
else:
    TEMPLATE_LOADERS = [
        ('django.template.loaders.cached.Loader',(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            )),
    ]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
	'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
#    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
	# 'django.middleware.csrf.CsrfViewMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	#'bc.context.common_context',
	'django.core.context_processors.static',
	'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages',
)


ROOT_URLCONF = 'bc.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
 #   '/home/qq6ka/bc/bc/templates/',
#    'C:/ksp/templates/flatpages/',
 # 'C:/mptt/bc/feincms/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
	'django.contrib.admin',
	'django.contrib.messages',
    'django.contrib.sites',
    'bc',
	'django.contrib.staticfiles',

)
