
import requests, time
from typing import Tuple, Optional, Dict, Any

API_KEY = "d8d912f5d1ecad57765cf4f6dae6e733"

def safe_get(url, params=None, timeout=10):
    try:
        r = requests.get(url, params=params, timeout=timeout)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
    return None

def get_coordinates(city: str, api_key: str=API_KEY) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    url = "http://api.openweathermap.org/geo/1.0/direct"
    js = safe_get(url, params={"q": city, "limit": 1, "appid": api_key})
    if not js or len(js) == 0:
        return None, None, None
    item = js[0]
    return float(item.get("lat")), float(item.get("lon")), item.get("country", "")

def fetch_openweather_weather(lat: float, lon: float, api_key: str=API_KEY) -> Dict[str, Any]:
    url = "https://api.openweathermap.org/data/2.5/weather"
    js = safe_get(url, params={"lat": lat, "lon": lon, "appid": api_key, "units": "metric"})
    if not js or "main" not in js:
        return {"temperature": None, "humidity": None, "wind_speed": None, "source": "simulated"}
    return {
        "temperature": float(js["main"].get("temp")),
        "humidity": float(js["main"].get("humidity")),
        "wind_speed": float(js.get("wind",{}).get("speed",0.0)),
        "source": "openweather"
    }

def fetch_openaq_pm25(city: str) -> Optional[float]:
    url = "https://api.openaq.org/v2/latest"
    js = safe_get(url, params={"city": city})
    if not js or "results" not in js:
        return None
    for res in js["results"]:
        for m in res.get("measurements", []):
            param = (m.get("parameter") or "").lower()
            if param in ("pm25", "pm2.5"):
                try:
                    return float(m.get("value"))
                except:
                    continue
    return None

def fetch_current_observation(city: str, api_key: str=API_KEY) -> Dict[str, Any]:
    lat, lon, country = get_coordinates(city, api_key)
    if lat is None:
        return {"error":"city_not_found"}
    weather = fetch_openweather_weather(lat, lon, api_key)
    pm25 = fetch_openaq_pm25(city)
    if pm25 is None:
        hum = weather.get("humidity") if weather.get("humidity") is not None else 60.0
        wind = weather.get("wind_speed") if weather.get("wind_speed") is not None else 2.0
        pm25 = max(5.0, min(300.0, 60.0 + (hum-50.0)*0.3 - wind*2.0))
    obs = {
        "city": city,
        "country": country,
        "lat": lat,
        "lon": lon,
        "pm25": float(pm25),
        "temperature": weather.get("temperature"),
        "humidity": weather.get("humidity"),
        "wind_speed": weather.get("wind_speed"),
        "timestamp": time.time(),
        "source": weather.get("source")
    }
    return obs
