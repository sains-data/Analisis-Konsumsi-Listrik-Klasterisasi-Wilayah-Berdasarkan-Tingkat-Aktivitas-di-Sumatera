import os
from typing import Optional

# Superset specific config
ROW_LIMIT = 5000
SUPERSET_WEBSERVER_PORT = 8088

# Flask App Builder configuration
# Secret key for signing cookies
SECRET_KEY = 'ThisIsNotASecretKeyForProduction'

# Database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://superset:superset@superset-db:5432/superset'

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = ''

# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': 'redis://redis:6379/1'
}

# Feature flags
FEATURE_FLAGS = {
    'ENABLE_TEMPLATE_PROCESSING': True,
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'DASHBOARD_FILTERS_EXPERIMENTAL': True,
    'ENABLE_EXPLORE_JSON_CSRF_PROTECTION': False,
    'ENABLE_EXPLORE_DRAG_AND_DROP': True,
    'GLOBAL_ASYNC_QUERIES': True,
    'VERSIONED_EXPORT': True,
    'ENABLE_TEMPLATE_REMOVE_FILTERS': True,
}

# CORS configuration
ENABLE_CORS = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['*']
}

# Default database for Superset metadata
class CeleryConfig(object):
    BROKER_URL = 'redis://redis:6379/0'
    CELERY_IMPORTS = ('superset.sql_lab', )
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    CELERYD_LOG_LEVEL = 'DEBUG'
    CELERYD_PREFETCH_MULTIPLIER = 10
    CELERY_ACKS_LATE = True

CELERY_CONFIG = CeleryConfig

# Async query configuration
RESULTS_BACKEND = {
    'cache_type': 'redis',
    'cache_default_timeout': 86400,  # 1 day
    'cache_redis_host': 'redis',
    'cache_redis_port': 6379,
    'cache_redis_db': 2,
}

# SQL Lab configuration
SQLLAB_CTAS_NO_LIMIT = True
SQLLAB_TIMEOUT = 300
SQLLAB_ASYNC_TIME_LIMIT_SEC = 300

# Email configuration (optional)
SMTP_HOST = 'localhost'
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = 'superset'
SMTP_PORT = 25
SMTP_PASSWORD = 'superset'
SMTP_MAIL_FROM = 'superset@superset.com'

# WebDriver configuration for chart screenshots
WEBDRIVER_BASEURL = 'http://superset:8088'
WEBDRIVER_BASEURL_USER_FRIENDLY = 'http://localhost:8088'

# Additional security
TALISMAN_ENABLED = False
WTF_CSRF_EXEMPT_LIST = []

# Custom CSS
CUSTOM_CSS = """
.navbar {
    background-color: #2c3e50 !important;
}
"""

# Dashboard auto-refresh intervals (in seconds)
SUPERSET_DASHBOARD_REFRESH_INTERVALS = [
    [10, '10 seconds'],
    [30, '30 seconds'],
    [60, '1 minute'],
    [300, '5 minutes'],
    [1800, '30 minutes'],
    [3600, '1 hour'],
    [21600, '6 hours'],
    [43200, '12 hours'],
    [86400, '24 hours'],
]

# Alert & Report frequency options
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
WEBDRIVER_TYPE = "firefox"
