from django.core.cache import cache

redis_client = cache.client.get_client()

def setRedisValue(key: str, value: str, expire: int = None) -> None:
    redis_client.set(key, value, ex=expire)

def getRedisValue(key: str) -> None | str:
    value: bytes = redis_client.get(key)
    if value:
        return value.decode('utf-8')

def getRedisKeyTTL(key: str) -> int | None:
    ttl = redis_client.ttl(key)
    if ttl not in [-2, -1]:
        return ttl