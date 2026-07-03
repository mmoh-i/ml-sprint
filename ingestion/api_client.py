import requests
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config  import BASE_URL, LATITUDE, LONGITUDE

def  fetch_weather(start_date: str, end_date: str) -> dict:

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,shortwave_radiation,wind_speed_10m,wind_direction_10m,wind_gusts_10m,relative_humidity_2m,rain,cloud_cover,soil_temperature_7_to_28cm,soil_moisture_7_to_28cm",
        "timezone": "Africa/Lagos"
    }

    response = requests.get(f"{BASE_URL}/archive", params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    data = fetch_weather("2026-07-01", "2026-07-03")
    print(f"fetched {len(data['hourly']['time'])} hourly records")
    print("Sample:", data['hourly']['time'][:3])