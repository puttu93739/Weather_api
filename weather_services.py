
import requests
import json
from config import VISUAL_CROSSING_API_KEY, CACHE_EXPIRY
from cache import get_cache, set_cache

def fetch_weather(city:str):
    cached = get_cache(city)
    if cached:
        return json.loads(cached)

    #if not in cache
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={VISUAL_CROSSING_API_KEY}"
    response = requests.get(url)

    if response.status_code!=200:
        return {"error":f"Failed to fetch weather data. Status code: {response.status_code}"}
    data = response.json()
    set_cache(city,json.dumps(data),CACHE_EXPIRY)
    return data