try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import os

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

SERVER_ALIAS = 'test'

# glance ini file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INI_DIR = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))
STATIC_ROOT = '/data/projects/resources/glance/static/'
# instantiate
config = ConfigParser()

config.read(os.path.join(INI_DIR, 'glance.ini'))

# test SECRET_KEY
SECRET_KEY = config.get('test', 'SECRET_KEY')
# for default db
default_db_user = config.get('test', 'default_db_user')
default_db_password = config.get('test', 'default_db_password')
default_db_host = config.get('test', 'default_db_host')
default_db_port = config.get('test', 'default_db_port')
#  for external db
external_db_user = config.get('test', 'external_db_user')
external_db_password = config.get('test', 'external_db_password')
external_db_host = config.get('test', 'external_db_host')
external_db_port = config.get('test', 'external_db_port')


DATABASES = {
    'default': {
        # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'glance',
        'USER': default_db_user,
        'PASSWORD': default_db_password,
        'HOST': default_db_host,
        'PORT': default_db_port,
        # Set this to True to wrap each HTTP request in a transaction on this
        # database.
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    },
    'external': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecmall',
        'USER': external_db_user,
        'PASSWORD': external_db_password,
        'HOST': external_db_host,
        'PORT': external_db_port,
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    },
}

