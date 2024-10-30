import os
from redis import Redis

cache = Redis(
    decode_responses=True,
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),
)
