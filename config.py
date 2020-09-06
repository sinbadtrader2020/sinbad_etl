import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG_TOOLBAR_ENABLED = True
    REST_URL_PREFIX = '/api'
    API_VERSION = '1'

    ADMIN_PASSWORD = ''
