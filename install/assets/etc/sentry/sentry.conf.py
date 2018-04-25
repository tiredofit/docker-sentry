# This file is just Python, with a touch of Django which means
# you can inherit and tweak settings to your hearts content.

# For Docker, the following environment variables are supported:
#  DB_HOST
#  DB_PORT
#  DB_NAME
#  DB_USER
#  DB_PASS
#  RABBITMQ_HOST
#  RABBITMQ_USER
#  RABBITMQ_PASS
#  RABBITMQ_VHOST
#  REDIS_HOST
#  REDIS_PASSW
#  REDIS_PORT
#  REDIS_DB
#  MEMCACHED_HOST
#  MEMCACHED_PORT
#  SENTRY_FILESTORE_DIR
#  SERVER_EMAIL
#  SMTP_HOST
#  SMTP_PORT
#  SMTP_USER
#  SMTP_PASS
#  SMTP_USE_TLS
#  ENABLE_EMAIL_REPLIES
#  SMTP_HOSTNAME
#  MAILGUN_API_KEY
#  SINGLE_ORGANIZATION
#  SECRET_KEY
#  GITHUB_APP_ID
#  GITHUB_API_SECRET
#  BITBUCKET_CONSUMER_KEY
#  BITBUCKET_CONSUMER_SECRET
from sentry.conf.server import *  # NOQA

import os
import os.path

CONF_ROOT = os.path.dirname(__file__)

postgres = env('DB_HOST') or (env('DB_PORT') and 'postgres')
if postgres:
    DATABASES = {
        'default': {
            'ENGINE': 'sentry.db.postgres',
            'NAME': (
                env('SENTRY_DB_NAME')
                or env('DB_NAME')
                or 'postgres'
            ),
            'USER': (
                env('SENTRY_DB_USER')
                or env('DB_USER')
                or 'postgres'
            ),
            'PASSWORD': (
                env('SENTRY_DB_PASSWORD')
                or env('DB_PASS')
                or ''
            ),
            'HOST': postgres,
            'PORT': (
                env('DB_PORT')
                or ''
            ),
            'OPTIONS': {
                'autocommit': True,
            },
        },
    }

# You should not change this setting after your database has been created
# unless you have altered all schemas first
SENTRY_USE_BIG_INTS = True

# If you're expecting any kind of real traffic on Sentry, we highly recommend
# configuring the CACHES and Redis settings

###########
# General #
###########

# Instruct Sentry that this install intends to be run by a single organization
# and thus various UI optimizations should be enabled.
SENTRY_SINGLE_ORGANIZATION = env('SINGLE_ORGANIZATION', True)

#########
# Redis #
#########

# Generic Redis configuration used as defaults for various things including:
# Buffers, Quotas, TSDB

redis = env('REDIS_HOST') or (env('REDIS_PORT') and 'redis')
if not redis:
    raise Exception('Error: REDIS_PORT (or REDIS_HOST) is undefined, did you forget to `--link` a redis container?')

redis_password = env('REDIS_PASS') or ''
redis_port = env('REDIS_PORT') or '6379'
redis_db = env('REDIS_DB') or '0'

SENTRY_OPTIONS.update({
    'redis.clusters': {
        'default': {
            'hosts': {
                0: {
                    'host': redis,
                    'password': redis_password,
                    'port': redis_port,
                    'db': redis_db,
                },
            },
        },
    },
})

#########
# Cache #
#########

# Sentry currently utilizes two separate mechanisms. While CACHES is not a
# requirement, it will optimize several high throughput patterns.

memcached = env('MEMCACHED_HOST') or (env('MEMCAHCED_PORT') and 'memcached')
if memcached:
    memcached_port = (
        env('MEMCACHED_PORT')
        or '11211'
    )
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [memcached + ':' + memcached_port],
            'TIMEOUT': 3600,
        }
    }

# A primary cache is required for things such as processing events
SENTRY_CACHE = 'sentry.cache.redis.RedisCache'

#########
# Queue #
#########

# See https://docs.getsentry.com/on-premise/server/queue/ for more
# information on configuring your queue broker and workers. Sentry relies
# on a Python framework called Celery to manage queues.

rabbitmq = env('RABBITMQ_HOST') or (env('RABBITMQ_PORT') and 'rabbitmq')

if rabbitmq:
    BROKER_URL = (
        'amqp://' + (
            env('RABBITMQ_USER')
            or env('RABBITMQ_ENV_RABBITMQ_DEFAULT_USER')
            or 'guest'
        ) + ':' + (
            env('RABBITMQ_PASS')
            or env('RABBITMQ_ENV_RABBITMQ_DEFAULT_PASS')
            or 'guest'
        ) + '@' + rabbitmq + '/' + (
            env('RABBITMQ_VHOST')
            or env('RABBITMQ_ENV_RABBITMQ_DEFAULT_VHOST')
            or '/'
        )
    )
else:
    BROKER_URL = 'redis://:' + redis_password + '@' + redis + ':' + redis_port + '/' + redis_db


###############
# Rate Limits #
###############

# Rate limits apply to notification handlers and are enforced per-project
# automatically.

SENTRY_RATELIMITER = 'sentry.ratelimits.redis.RedisRateLimiter'

##################
# Update Buffers #
##################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'

##########
# Quotas #
##########

# Quotas allow you to rate limit individual projects or the Sentry install as
# a whole.

SENTRY_QUOTAS = 'sentry.quotas.redis.RedisQuota'

########
# TSDB #
########

# The TSDB is used for building charts as well as making things like per-rate
# alerts possible.

SENTRY_TSDB = 'sentry.tsdb.redis.RedisTSDB'

###########
# Digests #
###########

# The digest backend powers notification summaries.

SENTRY_DIGESTS = 'sentry.digests.backends.redis.RedisBackend'

################
# File storage #
################

# Uploaded media uses these `filestore` settings. The available
# backends are either `filesystem` or `s3`.

SENTRY_OPTIONS['filestore.backend'] = 'filesystem'
SENTRY_OPTIONS['filestore.options'] = {
    'location': env('SENTRY_FILESTORE_DIR'),
}

##############
# Web Server #
##############

# If you're using a reverse SSL proxy, you should enable the X-Forwarded-Proto
# header and set `SENTRY_USE_SSL=1`

if env('SENTRY_USE_SSL', False):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    'workers': int(env('SENTRY_WORKERS') or 3),
    'limit_request_line': 0,  # required for raven-js
    'errorlog' : '/var/log/sentry/sentry_error.log',
    'accesslog' : '/var/log/sentry/sentry_access.log',
}

###############
# Mail Server #
###############
email = env('SMTP_HOST') or (env('SMTP_PORT') and 'smtp')
if email:
    SENTRY_OPTIONS['mail.backend'] = 'smtp'
    SENTRY_OPTIONS['mail.host'] = email
    SENTRY_OPTIONS['mail.password'] = env('SMTP_PASS') or ''
    SENTRY_OPTIONS['mail.username'] = env('SMTP_USER') or ''
    SENTRY_OPTIONS['mail.port'] = int(env('SMTP_PORT') or 25)
    SENTRY_OPTIONS['mail.use-tls'] = env('SMTP_USE_TLS', False)
else:
    SENTRY_OPTIONS['mail.backend'] = 'dummy'

# The email address to send on behalf of
SENTRY_OPTIONS['mail.from'] = env('SMTP_MAIL_FROM') or 'root@localhost'

# If you're using mailgun for inbound mail, set your API key and configure a
# route to forward to /api/hooks/mailgun/inbound/
SENTRY_OPTIONS['mail.mailgun-api-key'] = env('MAILGUN_API_KEY') or ''

# If you specify a MAILGUN_API_KEY, you definitely want EMAIL_REPLIES
if SENTRY_OPTIONS['mail.mailgun-api-key']:
    SENTRY_OPTIONS['mail.enable-replies'] = True
else:
    SENTRY_OPTIONS['mail.enable-replies'] = env('ENABLE_EMAIL_REPLIES', False)

if SENTRY_OPTIONS['mail.enable-replies']:
    SENTRY_OPTIONS['mail.reply-hostname'] = env('SMTP_HOSTNAME') or ''

# If this value ever becomes compromised, it's important to regenerate your
# SENTRY_SECRET_KEY. Changing this value will result in all current sessions
# being invalidated.
secret_key = env('SECRET_KEY')
if not secret_key:
    raise Exception('Error: SECRET_KEY is undefined, run `generate-secret-key` and set to -e SECRET_KEY')

if 'SENTRY_RUNNING_UWSGI' not in os.environ and len(secret_key) < 32:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('!!                    CAUTION                       !!')
    print('!! Your SECRET_KEY is potentially insecure.         !!')
    print('!!    We recommend at least 32 characters long.     !!')
    print('!!     Regenerate with `generate-secret-key`.       !!')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

SENTRY_OPTIONS['system.secret-key'] = secret_key
LOGGING['disable_existing_loggers'] = False
SENTRY_BEACON = env('BEACON', False)
SENTRY_FEATURES['auth:register'] = env('ALLOW_REGISTRATION',True)


if 'GITHUB_APP_ID' in os.environ:
    GITHUB_EXTENDED_PERMISSIONS = ['repo']
    GITHUB_APP_ID = env('GITHUB_APP_ID')
    GITHUB_API_SECRET = env('GITHUB_API_SECRET')

if 'BITBUCKET_CONSUMER_KEY' in os.environ:
    BITBUCKET_CONSUMER_KEY = env('BITBUCKET_CONSUMER_KEY')
    BITBUCKET_CONSUMER_SECRET = env('BITBUCKET_CONSUMER_SECRET')

SENTRY_FEATURES['organizations:sso'] = False
SENTRY_FEATURES['organizations:sso-saml2'] = False
SENTRY_FEATURES['organizations:sso-rippling'] = False
