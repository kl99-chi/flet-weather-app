# Flet Weather App

A phone-sized weather app built with Python and [Flet](https://flet.dev). Search any city and see its current temperature, conditions, humidity and wind, powered by the OpenWeatherMap API.

Built as the capstone of the **FNB App Academy 2026** (app development module, with the University of Johannesburg).

## Features
- City search by button click or the Enter key
- Temperature (°C, rounded), conditions icon, humidity and wind speed (km/h)
- Friendly errors: empty input, city not found, bad API key, network failure
- API key kept out of the code through a `.env` file

## What I practised
REST API integration, `try/except` error handling, functions returning dictionaries, state management and event handling in Flet, environment variables for secrets.

## Run it
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then paste your free OpenWeatherMap key
python src/main.py
```
Get a free key at https://openweathermap.org/api (new keys can take a little while to activate).

## Project structure
```
src/main.py       the whole app: API function, UI, event handling
.env.example      template for your API key (never commit the real .env)
requirements.txt  dependencies
```

## Ideas for next steps
Five-day forecast, geolocation, °C/°F toggle, recent searches.
