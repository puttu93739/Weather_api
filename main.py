from fastapi import FastAPI,HTTPException,Request
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from weather_services import fetch_weather

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.get("/weather/{city}")
@limiter.limit("5/minute")
async def get_weather(city:str,request:Request):
    """
    Endpoint to fetch weather information for a given city.

    This endpoint is rate-limited to 5 requests per minute per client.

    Args:
        city (str): The name of the city for which to fetch weather data.
        request (Request): The HTTP request object, used to identify the client.

    Returns:
        dict: A dictionary containing weather data for the specified city.

    Raises:
        HTTPException: If an error occurs while fetching weather data,
                       a 502 Bad Gateway error is returned with the error details.
    """
    data =fetch_weather(city)
    if "error" in data:
        raise HTTPException(status_code=502,detail=data['error'])
    return data