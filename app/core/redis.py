import redis.asyncio as aioredis
from typing import Any, Optional
import json

from .config import settings

DEFAULT_EXPIRY = 3600  # 

# Shared Redis instance
try:
    redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    print("Connected to Redis successfully.")
except Exception as e:
    print(f"Failed to connect to Redis: {e}")
    redis_client = None

# --- Token Blocklist (JWT JTI Blacklisting) ---
JTI_EXPIRY = 3600  # 1 hour

async def add_jti_to_blocklist(jti: str) -> None:
    if redis_client is None:
        raise ConnectionError("Redis client is not initialized.")
    await redis_client.set(name=jti, value="", ex=JTI_EXPIRY)

async def token_in_blocklist(jti: str) -> bool:
    if redis_client is None:
        raise ConnectionError("Redis client is not initialized.")
    return await redis_client.get(jti) is not None


# --- General Cache Utilities ---

async def set_cache(key: str, value: Any, expiry: int = DEFAULT_EXPIRY) -> None:
    if redis_client is None:
        raise ConnectionError("Redis client is not initialized.")
    serialized = json.dumps(value)
    await redis_client.set(name=key, value=serialized, ex=expiry)

async def get_cache(key: str) -> Optional[Any]:
    if redis_client is None:
        raise ConnectionError("Redis client is not initialized.")
    value = await redis_client.get(key)
    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value

async def invalidate_cache(key: str) -> None:
    if redis_client is None:
        raise ConnectionError("Redis client is not initialized.")
    await redis_client.delete(key)
