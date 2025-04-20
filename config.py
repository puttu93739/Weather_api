from dotenv import load_dotenv
import os

load_dotenv()

VISUAL_CROSSING_API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
REDIS_URL = os.getenv("REDIS_URL")
CACHE_EXPIRY = int(os.getenv("CACHE_EXPIRY", 43200))
