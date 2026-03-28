# weather_mcp_server_weatherapi.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import requests

load_dotenv()
app = FastAPI()

API_KEY = os.getenv('WEATHER_API_KEY')


# -------- Request Schema --------
class WeatherRequest(BaseModel):
    location: str


# -------- 🌤 Current Weather Tool --------
@app.post("/tools/get_current_weather")
def get_current_weather(req: WeatherRequest):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={req.location}&aqi=no"
    res = requests.get(url).json()

    if "error" in res:
        return {"error": res["error"]["message"]}

    return {
        "location": res["location"]["name"],
        "region": res["location"]["region"],
        "country": res["location"]["country"],
        "temperature_c": res["current"]["temp_c"],
        "feels_like_c": res["current"]["feelslike_c"],
        "condition": res["current"]["condition"]["text"],
        "humidity": res["current"]["humidity"],
        "wind_kph": res["current"]["wind_kph"]
    }


# -------- 🌦 Forecast Tool --------
@app.post("/tools/get_forecast")
def get_forecast(req: WeatherRequest):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={req.location}&days=3&aqi=no&alerts=no"
    res = requests.get(url).json()

    if "error" in res:
        return {"error": res["error"]["message"]}

    forecast_days = []

    for day in res["forecast"]["forecastday"]:
        forecast_days.append({
            "date": day["date"],
            "avg_temp_c": day["day"]["avgtemp_c"],
            "condition": day["day"]["condition"]["text"],
            "max_temp_c": day["day"]["maxtemp_c"],
            "min_temp_c": day["day"]["mintemp_c"]
        })

    return {
        "location": res["location"]["name"],
        "forecast": forecast_days
    }


# -------- Health Check --------
@app.get("/")
def home():
    return {"status": "WeatherAPI MCP Server running 🌍🚀"}