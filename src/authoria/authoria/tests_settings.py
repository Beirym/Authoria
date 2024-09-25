from .settings import *

# Database
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
   }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100,
            },
        }
    }
}