from os import environ
from os.path import dirname, realpath

timeout = 300
bind = "127.0.0.1:8000"
pythonpath = environ.get('AMA_HOME', dirname(realpath(__file__)))
daemon = False
workers = 2
loglevel = "debug"
