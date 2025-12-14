import redis.asyncio as redis

from app.config import settings


async_redis_client = redis.Redis(
    host=settings.REDIS_HOST, port=int(settings.REDIS_PORT), db=int(settings.REDIS_DB)
)
