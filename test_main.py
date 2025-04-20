
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

# Sample mock response from external API
mock_response = {
  "data": {
    "time": "2025-04-09T19:18:00Z",
    "values": {
      "cloudBase": 0.9,
      "cloudCeiling": 0.9,
      "cloudCover": 76,
      "dewPoint": 3.8,
      "freezingRainIntensity": 0,
      "humidity": 61,
      "precipitationProbability": 0,
      "pressureSeaLevel": 1030.38,
      "pressureSurfaceLevel": 1027.85,
      "rainIntensity": 0,
      "sleetIntensity": 0,
      "snowIntensity": 0,
      "temperature": 11,
      "temperatureApparent": 11,
      "uvHealthConcern": 0,
      "uvIndex": 0,
      "visibility": 16,
      "weatherCode": 1001,
      "windDirection": 46,
      "windGust": 7.6,
      "windSpeed": 3.2
    }
  },
  "location": {
    "lat": 51.51561737060547,
    "lon": -0.09199830144643784,
    "name": "City of London, Greater London, England, United Kingdom",
    "type": "administrative"
  }
}
# Test successful weather fetch
@patch("weather_services.fetch_weather")
@patch("cache.get_cache", return_value=None)
@patch("cache.set_cache")
def test_get_weather_success(mock_set, mock_cache, mock_weather):
    mock_weather.return_value = mock_response
    response = client.get("/weather/London")
    assert response.status_code == 200
    # assert response.json()["city"] == "London"

# Test when data is in Redis cache
@patch("weather_services.fetch_weather")
@patch("cache.get_cache", return_value=mock_response)
def test_get_weather_from_cache(mock_cache, mock_weather):
    response = client.get("/weather/London")
    assert response.status_code == 200
    # assert response.json()["city"] == "London"
    mock_weather.assert_not_called()

# Test invalid city or API error
@patch("weather_services.fetch_weather", side_effect=Exception("API error"))
@patch("cache.get_cache", return_value=None)
def test_invalid_city(mock_cache, mock_weather):
    response = client.get("/weather/InvalidCity")
    assert response.status_code == 500
    assert "error" in response.json()

# Test rate limiting: simulate more than 5 requests/minute
def test_rate_limit():
    for _ in range(5):
        res = client.get("/weather/London")
        assert res.status_code in [200, 429]  # Could be a mix if run fast

    # 6th request should fail
    res = client.get("/weather/London")
    assert res.status_code == 429
