
import json, os

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "aqi_model.json")

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH,"r",encoding="utf-8") as f:
            return json.load(f)
    return {"model_type":"linear","intercept":0.0,"coefficients":{"pm25":0.8,"temperature":0.2,"humidity":-0.1,"wind_speed":0.5,"hours_ahead":0.1}}

def predict(model, obs, hours_ahead:int):
    coef = model.get("coefficients",{})
    intercept = float(model.get("intercept",0.0))
    total = intercept
    total += float(coef.get("pm25",0.0)) * float(obs["pm25"])
    total += float(coef.get("temperature",0.0)) * float(obs.get("temperature") or 25.0)
    total += float(coef.get("humidity",0.0)) * float(obs.get("humidity") or 60.0)
    total += float(coef.get("wind_speed",0.0)) * float(obs.get("wind_speed") or 2.0)
    total += float(coef.get("hours_ahead",0.0)) * float(hours_ahead)
    return float(max(0,min(500,total)))
