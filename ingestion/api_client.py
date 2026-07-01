import requests
from config  import BASE_URL, LATITUDE, LONGITUDE

def  fetch_weather(start_date: str, end_date: str) -> dict:

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,shortwave_radiation,wind_speed_10m,relative_humidity_2m",
        "timezone": "Africa/Lagos"
    }

    response = requests.get(f"{BASE_URL}/forecast", params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    data = fetch_weather("2026-07-01", "2026-07-03")
    print(f"fetched {len(data['hourly']['time'])} hourly records")
    print("Sample:", data['hourly']['time'][:3])