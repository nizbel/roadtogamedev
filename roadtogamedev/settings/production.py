from .base import *

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('SITE_NAME'),]

try:
    from .local import *
except ImportError:
    pass
