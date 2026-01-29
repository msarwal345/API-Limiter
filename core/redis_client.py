import redis
from django.conf import settings


def get_redis():
    redis_client = redis.Redis.from_url(settings.CACHES["default"]["LOCATION"])
    return redis_client