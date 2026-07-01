import os
from dotenv import load_dotenv


load_dotenv()

BASE_URL = os.getenv("OPEN_MATEO_BASE_URL")
LATITUDE = float(os.getenv("STATION_LATITUDE"))
LONGTITUDE = float(os.getenv("STATION_LONGTITUDE"))