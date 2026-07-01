import os
from dotenv import load_dotenv


load_dotenv()

BASE_URL = os.getenv("OPEN_METEO_BASE_URL")
LATITUDE = float(os.getenv("STATION_LATITUDE"))
LONGITUDE = float(os.getenv("STATION_LONGITUDE"))