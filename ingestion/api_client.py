import requests
from config  import BASE_URL, LATITUDE, LONGTITUDE

def  fetch_weather(start_date: str, end_date: str) -> dict:

    params = {
        "latitude": LATITUDE,
        "longtitude": LONGTITUDE,
        "start_date": start_date,
        "end_dte": end_date,
        "hourly": "temprature_2m, shortwave_radiation, windspeed_10m, relativehumidity_2m",
        "timezone": "Africa/Lagos"
    }

    response = requests.get(f"{BASE_URL}/forecast", params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    data = fetch_weather("")
    print(f"fetched {len(data['hourly']['time'])} hourly records")
    print("Sample:", data['hourly']['time'][:3])