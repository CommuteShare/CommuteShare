from .common import *
DEBUG = True

SECRET_KEY = 'django-insecure-xi9dkp$ot@+s2y_q$o4wchpt6vi)g%14lzx#-_8bmbd9af_byt'

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
    }
}

