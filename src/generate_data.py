import pandas as pd
import random

cities = [
    "Delhi",
    "Mumbai",
    "Jaipur",
    "Kolkata",
    "Chennai",
    "Bangalore",
    "Pune",
    "Hyderabad"
]

conditions = [
    "Sunny",
    "Cloudy",
    "Rain",
    "Heavy Rain",
    "Mist",
    "Clear Sky"
]

data = []

for city in cities:

    temperature = random.randint(25, 45)
    humidity = random.randint(40, 95)
    condition = random.choice(conditions)
    wind_speed = random.randint(2, 15)

    data.append({
        "City": city,
        "Temperature": temperature,
        "Humidity": humidity,
        "Condition": condition,
        "WindSpeed": wind_speed
    })

df = pd.DataFrame(data)

df.to_csv("data/synthetic_weather_data.csv", index=False)

print("Synthetic weather dataset generated successfully.")