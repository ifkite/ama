#! encoding=UTF-8
'''
debug开发配置
'''

from common import *
from os import environ
from os.path import dirname, realpath, join


# 使用默认mongo配置，默认端口，无密码
MONGO_HOST = "127.0.0.1"
MONGO_DATABASE = "debug_ama"
MONGO_USER = ""
MONGO_PASSWORD = ""

DEBUG = True
try:
    LOG_PATH = join(dirname(environ.get('AMA_HOME', dirname(dirname(realpath(__file__))))), 'var/log')
except AttributeError:
    print 'source ama_env first'
LOG_NAME = 'ama.log'
