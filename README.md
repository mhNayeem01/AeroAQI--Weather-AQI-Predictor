# 🌤️ Weather & AQI Predictor

A simple **Streamlit web app** that fetches real-time weather information using the [OpenWeatherMap API](https://openweathermap.org/api) and predicts the **Air Quality Index (AQI)** using a machine learning model.  
The app also lets you forecast the AQI **n hours into the future**.

---

## 📌 Features
- 🌍 Enter any **city name** to get live weather data  
- 📊 Predict **current AQI** based on weather conditions  
- ⏳ Forecast **future AQI after n hours**  
- 🎥 Includes a demo video  

---

## 📽️ Demo
<p align="center">
  <video src="src/demo.mp4" controls width="700"></video>
</p>

---

## 🛠️ Tech Stack
- [Streamlit](https://streamlit.io/) – Web UI  
- [OpenWeatherMap API](https://openweathermap.org/api) – Weather data  
- [Scikit-learn](https://scikit-learn.org/) – AQI prediction model  
- Python (NumPy, Pandas, Requests)  

---

## 🚀 Installation & Usage

### 1️⃣ Clone this repository
```bash
git clone https://github.com/your-username/weather-aqi-app.git
cd weather-aqi-app
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the app
```bash
streamlit run app.py
```

## Contributing

Pull requests are welcome! You can use your own api key, as my api is free trial and limited. For major changes, please open an issue first to discuss what you’d like to change.
