# Weather_api
Weather from extrenal apis
https://roadmap.sh/projects/weather-api-wrapper-service

# Weather API

A FastAPI-based application to fetch real-time weather data for a given city using external APIs. The application includes rate-limiting and caching mechanisms to optimize performance and API usage.

## Features

- Fetch real-time weather data for any city.
- Rate-limited to 5 requests per minute per client.
- Caching support to reduce redundant API calls.
- Error handling for failed API requests.

## Requirements

- Python 3.8+
- Redis (for caching)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd weather_api
   
Install dependencies:

pip install -r requirements.txt