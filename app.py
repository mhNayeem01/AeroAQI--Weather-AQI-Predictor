
import streamlit as st
import os, time
from src.data_sources import fetch_current_observation
from src.model import load_model, predict

API_KEY = "108b1a451bff4c206f9afcafb684ba2b"

st.set_page_config(page_title="AirQ Forecast", page_icon="🌍", layout="wide")
st.title("🌍 AirQ - Current AQI + Hours-ahead Prediction")

st.sidebar.header("Settings")
city = st.sidebar.text_input("City name", value="Dhaka")
hours = st.sidebar.number_input("Hours ahead to predict", min_value=0, max_value=168, value=3, step=1)

st.write("Enter a city name and choose how many hours ahead you want to predict the AQI for.")

if st.button("Fetch & Predict"):
    with st.spinner("Fetching current observation..."):
        obs = fetch_current_observation(city, API_KEY)
    if obs.get("error") == "city_not_found":
        st.error("City not found. Check name spelling.")
    else:
        st.metric("Current PM2.5 (µg/m3)", f"{obs['pm25']:.1f}")
        st.metric("Temperature (°C)", f"{obs['temperature']:.1f}" if obs.get('temperature') is not None else "-")
        st.metric("Humidity (%)", f"{obs['humidity']:.1f}" if obs.get('humidity') is not None else "-")
        st.metric("Wind (m/s)", f"{obs['wind_speed']:.1f}" if obs.get('wind_speed') is not None else "-")
        # save observation to CSV
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)
        csv_path = os.path.join(data_dir, "realtime_data.csv")
        import csv, datetime
        write_header = not os.path.exists(csv_path)
        with open(csv_path, "a", newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(["timestamp","city","lat","lon","pm25","temperature","humidity","wind_speed"])
            w.writerow([datetime.datetime.utcnow().isoformat()+"Z", obs['city'], obs['lat'], obs['lon'], obs['pm25'], obs.get('temperature'), obs.get('humidity'), obs.get('wind_speed')])
        # load model and predict
        model = load_model()
        pred = predict(model, obs, int(hours))
        st.subheader(f"Predicted AQI after {hours} hour(s): {pred:.1f}")
        st.caption("Model type: " + model.get('model_type','linear'))
