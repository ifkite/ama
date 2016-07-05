#! encoding=UTF-8
'''
线上配置
'''

from common import *
from os import environ
from os.path import dirname, realpath, join

MONGO_HOST = ""
MONGO_DATABASE = "ama"
MONGO_USER = ""
MONGO_PASSWORD = ""

DEBUG = False
try:
    LOG_PATH = join(dirname(environ.get('AMA_HOME', dirname(dirname(realpath(__file__))))), 'var/log')
except AttributeError:
    print 'source ama_env first'
LOG_NAME = 'ama.log'
