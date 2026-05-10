import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "http://api.weatherapi.com/v1/current.json"

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Weather Forecast & Alert App",
    layout="wide"
)

st.title("🌦 Weather Forecast & Alert Application")

st.write("Live Weather Monitoring + Alert System")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Settings")

mode = st.sidebar.selectbox(
    "Select Mode",
    ["Live API Mode", "Simulation Mode"]
)

city = st.sidebar.text_input("Enter City Name", "Delhi")

temp_threshold = st.sidebar.slider(
    "Temperature Alert Threshold",
    20,
    50,
    35
)

humidity_threshold = st.sidebar.slider(
    "Humidity Alert Threshold",
    40,
    100,
    80
)

# ==========================================
# FETCH LIVE WEATHER
# ==========================================

def fetch_weather(city):

    params = {
        "key": API_KEY,
        "q": city
    }

    response = requests.get(BASE_URL, params=params)

    data = response.json()

    if response.status_code == 200:
        return data

    else:
        st.error("Weather API Error")
        return None


# ==========================================
# LOAD SIMULATION DATA
# ==========================================

def load_simulation_data():

    with open("data/sample_weather.json", "r") as file:
        data = json.load(file)

    return data


# ==========================================
# GET WEATHER DATA
# ==========================================

if st.sidebar.button("Get Weather"):

    # ======================================
    # LIVE API MODE
    # ======================================

    if mode == "Live API Mode":

        data = fetch_weather(city)

        if data is None:

            st.warning("Switching to Simulation Mode")

            data = load_simulation_data()

    # ======================================
    # SIMULATION MODE
    # ======================================

    else:

        data = load_simulation_data()

    # ======================================
    # EXTRACT WEATHER DATA
    # ======================================

    city_name = data["location"]["name"]

    temperature = data["current"]["temp_c"]

    humidity = data["current"]["humidity"]

    condition = data["current"]["condition"]["text"]

    wind_speed = data["current"]["wind_kph"]

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ======================================
    # WEATHER CARDS
    # ======================================

    st.subheader("📋 Current Weather")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🌡 Temperature", f"{temperature} °C")

    col2.metric("💧 Humidity", f"{humidity}%")

    col3.metric("🌬 Wind Speed", f"{wind_speed} kph")

    col4.metric("☁ Condition", condition)

    st.write("🕒 Time:", current_time)

    # ======================================
    # ALERT SYSTEM
    # ======================================

    st.subheader("⚠ Weather Alerts")

    alert_found = False

    if temperature > temp_threshold:
        st.warning("High Temperature Alert")
        alert_found = True

    if humidity > humidity_threshold:
        st.warning("High Humidity Alert")
        alert_found = True

    if "rain" in condition.lower():
        st.warning("Rain Alert")
        alert_found = True

    if "storm" in condition.lower():
        st.error("Storm Alert")
        alert_found = True

    if not alert_found:
        st.success("No Alerts")

    # ======================================
    # DATAFRAME
    # ======================================

    weather_df = pd.DataFrame({
        "Parameter": [
            "Temperature",
            "Humidity",
            "Wind Speed"
        ],

        "Value": [
            temperature,
            humidity,
            wind_speed
        ]
    })

    st.subheader("📊 Weather Data Table")

    st.dataframe(weather_df)

    # ======================================
    # BAR CHART
    # ======================================

    st.subheader("📈 Weather Analysis Chart")

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(
        weather_df["Parameter"],
        weather_df["Value"]
    )

    ax.set_ylabel("Values")

    ax.set_title(f"Weather Analysis - {city_name}")

    st.pyplot(fig)

    # ======================================
    # LINE CHART (SIMULATED FORECAST)
    # ======================================

    st.subheader("📉 5-Day Simulated Forecast")

    forecast_days = [
        "Day 1",
        "Day 2",
        "Day 3",
        "Day 4",
        "Day 5"
    ]

    forecast_temp = [
        temperature,
        temperature + 1,
        temperature - 2,
        temperature + 3,
        temperature - 1
    ]

    forecast_df = pd.DataFrame({
        "Day": forecast_days,
        "Temperature": forecast_temp
    })

    st.line_chart(
        forecast_df.set_index("Day")
    )

    # ======================================
    # SAVE CSV REPORT
    # ======================================

    os.makedirs("outputs", exist_ok=True)

    report_df = pd.DataFrame({

        "City": [city_name],

        "Temperature": [temperature],

        "Humidity": [humidity],

        "Wind Speed": [wind_speed],

        "Condition": [condition],

        "Date": [current_time]
    })

    report_path = "outputs/weather_report.csv"

    report_df.to_csv(report_path, index=False)

    # ======================================
    # DOWNLOAD BUTTON
    # ======================================

    st.download_button(
        label="⬇ Download Weather Report CSV",
        data=report_df.to_csv(index=False),
        file_name="weather_report.csv",
        mime="text/csv"
    )

    st.success("Weather Report Generated Successfully")
    # ....