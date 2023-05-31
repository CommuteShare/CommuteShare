from .common import *
DEBUG = True

SECRET_KEY = 'django-insecure-xi9dkp$ot@+s2y_q$o4wchpt6vi)g%14lzx#-_8bmbd9af_byt'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':'commute_sharedb',
        'USER': 'postgres',
        'PASSWORD': 'simex',
        'HOST': 'localhost',
        'PORT': '5432',

    }
}