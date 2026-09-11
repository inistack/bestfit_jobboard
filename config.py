import os


def _str_to_bool(s):
    return s.lower() in ('true', '1')


class Config:
    DEBUG = _str_to_bool(os.environ.get('FLASK_DEBUG', 'False'))
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql://jobboard:jobboard@localhost:5432/jobboard")
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'my_jwt_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_TITLE = 'BestFit Job Board API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.3'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_SWAGGER_UI_PATH = '/docs'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    RATELIMIT_STORAGE_URI = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'sandbox.smtp.mailtrap.io')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 2525))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@bestfitjobboard.com')
    S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL', 'http://localhost:9000')
    S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY', 'minioadmin')
    S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY', 'minioadmin')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'application-pdfs')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', "postgresql://jobboard:jobboard@localhost:5432/jobboard_test")
    TESTING = True
    RATELIMIT_ENABLED = False

class TestingConfigWithRateLimit(TestingConfig):
    RATELIMIT_ENABLED = True