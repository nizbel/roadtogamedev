from .base import *

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('SITE_NAME'),]

try:
    from .local import *
except ImportError:
    pass

MEDIA_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'