from django.conf import settings


def make_cache_key(key, key_prefix=settings.KEY_PREFIX, version=settings.CACHE_VERSION):
    return f"{key_prefix}:{version}:{key}"
