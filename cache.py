import redis
from config import REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def get_cache(city: str):
    return redis_client.get(city)


def set_cache(city: str, data: str, expiry: int):
    return redis_client.set(city, data, ex=expiry)
