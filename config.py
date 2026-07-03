import os
from dotenv import load_dotenv


load_dotenv()

BASE_URL = os.getenv("OPEN_METEO_BASE_URL")
LATITUDE = float(os.getenv("STATION_LATITUDE"))
LONGITUDE = float(os.getenv("STATION_LONGITUDE"))

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"