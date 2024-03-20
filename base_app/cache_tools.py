import json

import redis
from django.conf import settings


def update_cache_key(cache, key, value):
    if key in cache:
        cache.delete(key)
    json_value = json.dumps(value)
    cache.set(key, json_value)


def get_object_from_cache(cache, key):
    if key in cache:
        return json.loads(cache.get(key))
    return None


def remove_cache_key(cache, key):
    if key in cache:
        cache.delete(key)


def db_move_redis_key(source_cache, target_cache, key):
    # cluster case - move a key from the temp cache to the base cache as Python obj - different cache instances
    if settings.REDIS_RUNS_IN_CLUSTER:
        temp_data = get_object_from_cache(source_cache, key)
        update_cache_key(target_cache, key, temp_data)
        remove_cache_key(source_cache, key)
        return

    # non-cluster case - move key directly - same cache instance
    target_cache_db = target_cache.connection_pool.connection_kwargs.get('db')
    if key not in source_cache:
        return
    if key in target_cache:
        target_cache.delete(key)
    source_cache.move(key, target_cache_db)


_base_cache = getattr(redis, 'RedisCluster') if settings.REDIS_RUNS_IN_CLUSTER else getattr(redis, 'StrictRedis')
BASE_CACHE = _base_cache(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASS,
    ssl=settings.REDIS_SSL,
)

TEMP_CACHE = redis.StrictRedis(
    host=settings.REDIS_TEMP_HOST if settings.REDIS_RUNS_IN_CLUSTER else settings.REDIS_HOST,
    port=settings.REDIS_TEMP_PORT if settings.REDIS_RUNS_IN_CLUSTER else settings.REDIS_PORT,
    password=settings.REDIS_TEMP_PASS if settings.REDIS_RUNS_IN_CLUSTER else settings.REDIS_PASS,
    ssl=settings.REDIS_TEMP_SSL if settings.REDIS_RUNS_IN_CLUSTER else settings.REDIS_SSL,
    db=15,
)
