"""
Django settings for tuanchego project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def local_path(path):
    return os.path.join(os.path.dirname(__file__), os.pardir, path)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i@)fp3#=5sg^o*=vftdnj@5rz5sg@+60y58)r-!==7-a6l589@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xadmin',
    'crispy_forms',
    'data',
    'users',
    'cars',
    'activities',
    'django_cron'

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tuanchego.urls'

WSGI_APPLICATION = 'tuanchego.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default.back': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cars',
        'USER': 'cars',
        'PASSWORD': '123456',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Chongqing'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

XADMIN_CONF = 'tuanchego.xsite'

#STATIC_ROOT ='/home/yu/tuanchego/tuanchego/backend/tuanchego/static'# os.environ.get('STATIC_ROOT', local_path('static/'))
STATICFILES_DIRS = (
  os.environ.get('STATIC_ROOT', local_path('static/')),
)
#import pdb
#pdb.set_trace()

CRON_CLASSES = [
    #"cars.cron.GetBrandJob",
    #"cars.cron.GetCarJob",
    #"cars.cron.RefreshCarPriceJob",
    #"cars.cron.RefreshCarSizeJob",
    #"cars.cron.RefreshCarGearboxJob",
    #"cars.cron.RefreshCarDispatchJob",
    #"cars.cron.RefreshCarOriginJob",
    #"cars.cron.DownloadCarImgs",
    "cars.cron.DownLoadPageImages",
    # ...
]
