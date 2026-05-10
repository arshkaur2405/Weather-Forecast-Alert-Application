import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "http://api.weatherapi.com/v1/current.json"

# Alert Thresholds
TEMP_THRESHOLD = 35
HUMIDITY_THRESHOLD = 80


# ==========================================
# FETCH LIVE WEATHER
# ==========================================

def fetch_weather(city):

    params = {
        "key": API_KEY,
        "q": city
    }

    try:

        response = requests.get(BASE_URL, params=params)

        data = response.json()

        if response.status_code == 200:
            return data

        else:
            print("\nLive API Error:")
            print(data.get("error", {}).get("message"))

            return None

    except Exception as e:
        print("Exception:", e)
        return None


# ==========================================
# LOAD SIMULATION DATA
# ==========================================

def load_simulation_data():

    with open("data/sample_weather.json", "r") as file:
        data = json.load(file)

    return data


# ==========================================
# PARSE WEATHER DATA
# ==========================================

def parse_weather(data):

    weather_info = {

        "city": data["location"]["name"],

        "temperature": data["current"]["temp_c"],

        "humidity": data["current"]["humidity"],

        "condition": data["current"]["condition"]["text"],

        "wind_speed": data["current"]["wind_kph"],

        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return weather_info


# ==========================================
# GENERATE ALERTS
# ==========================================

def generate_alerts(weather_info):

    alerts = []

    if weather_info["temperature"] > TEMP_THRESHOLD:
        alerts.append("High Temperature Alert")

    if weather_info["humidity"] > HUMIDITY_THRESHOLD:
        alerts.append("High Humidity Alert")

    if "rain" in weather_info["condition"].lower():
        alerts.append("Rain Alert")

    if "storm" in weather_info["condition"].lower():
        alerts.append("Storm Alert")

    return alerts


# ==========================================
# DISPLAY WEATHER
# ==========================================

def display_weather(weather_info, alerts):

    print("\n========== WEATHER REPORT ==========")

    print(f"City: {weather_info['city']}")

    print(f"Temperature: {weather_info['temperature']} °C")

    print(f"Humidity: {weather_info['humidity']}%")

    print(f"Condition: {weather_info['condition']}")

    print(f"Wind Speed: {weather_info['wind_speed']} kph")

    print(f"Date & Time: {weather_info['date_time']}")

    print("\n========== ALERTS ==========")

    if alerts:

        for alert in alerts:
            print(f"⚠ {alert}")

    else:
        print("No Alerts")


# ==========================================
# SAVE CSV REPORT
# ==========================================

def save_report(weather_info, alerts):

    os.makedirs("outputs", exist_ok=True)

    data = {
        "City": [weather_info["city"]],
        "Temperature": [weather_info["temperature"]],
        "Humidity": [weather_info["humidity"]],
        "Condition": [weather_info["condition"]],
        "Wind Speed": [weather_info["wind_speed"]],
        "Alerts": [", ".join(alerts)],
        "Date": [weather_info["date_time"]]
    }

    df = pd.DataFrame(data)

    file_path = "outputs/weather_report.csv"

    df.to_csv(file_path, index=False)

    print(f"\nCSV Report Saved: {file_path}")


# ==========================================
# CREATE VISUALIZATION
# ==========================================

def plot_weather(weather_info):

    os.makedirs("images", exist_ok=True)

    labels = ["Temperature", "Humidity"]

    values = [
        weather_info["temperature"],
        weather_info["humidity"]
    ]

    plt.figure(figsize=(6, 4))

    plt.bar(labels, values)

    plt.title(f"Weather Analysis - {weather_info['city']}")

    plt.ylabel("Values")

    image_path = "images/weather_chart.png"

    plt.savefig(image_path)

    print(f"Chart Saved: {image_path}")


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():

    print("\n====== WEATHER FORECAST & ALERT APPLICATION ======")

    print("\n1. Live API Mode")
    print("2. Simulation Mode")

    choice = input("\nSelect mode: ")

    # ======================================
    # LIVE API MODE
    # ======================================

    if choice == "1":

        city = input("\nEnter city name: ")

        data = fetch_weather(city)

        if data is None:

            print("\nSwitching to Simulation Mode...")

            data = load_simulation_data()

    # ======================================
    # SIMULATION MODE
    # ======================================

    elif choice == "2":

        data = load_simulation_data()

    else:
        print("Invalid Choice")
        return

    # Process weather data
    weather_info = parse_weather(data)

    # Generate alerts
    alerts = generate_alerts(weather_info)

    # Display output
    display_weather(weather_info, alerts)

    # Save report
    save_report(weather_info, alerts)

    # Create chart
    plot_weather(weather_info)


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":
    main()