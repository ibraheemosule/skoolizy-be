import os
from redis import Redis

from dotenv import load_dotenv

load_dotenv()

cache = Redis(
    decode_responses=True,
    host=str(os.getenv('REDIS_HOST')),
    port=int(os.getenv('REDIS_PORT')),
    password=str(os.getenv('REDIS_PASSWORD')),
)
