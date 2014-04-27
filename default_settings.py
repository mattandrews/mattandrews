CACHE_DIR = "/Users/matt/Dev/www/mattandrews/CACHE/"
STATIC_URL = 'http://localhost/mattandrews/'
DEBUG = True
DEFAULT_CACHE = 0

try:
    from local_settings import *
except ImportError:
    # no local config found
    pass