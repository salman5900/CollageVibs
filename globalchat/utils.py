import os
import redis
from urllib.parse import urlparse

# Get Redis URL from env or default to Upstash (for local: set REDIS_URL manually)
redis_url = os.environ.get(
    "REDIS_URL",
    "rediss://default:AXdrAAIjcDFhY2I0YmVlMzQ0YjI0MWJmYjFiMTQ1NjRiZWU1NDVkY3AxMA@evolved-cricket-30571.upstash.io:6379"
)
parsed_url = urlparse(redis_url)

# Universal redis_instance
redis_instance = redis.StrictRedis(
    host=parsed_url.hostname,
    port=parsed_url.port,
    password=parsed_url.password,
    db=0,
    decode_responses=True,
    ssl=parsed_url.scheme == 'rediss'
)
