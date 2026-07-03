import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, Column, Float, String, DateTime, Integer,text
from sqlalchemy.orm import declarative_base, Session
from config import DATABASE_URL
from ingestion.api_client import fetch_weather

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

#Table

class WeatherReading(Base):
    """
    One row = one hourly reading from one station.
    This schema carries you through all 30 days unchanged.
    """
    __tablename__ = "weather_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    station_id = Column(String, nullable=False)
    temperature_2m = Column(Float)
    shortwave_radiation = Column(Float)
    windspeed_10m = Column(Float)
    wind_direction_10m = Column(Float)
    wind_gusts_10m = Column(Float)
    relative_humidity_2m = Column(Float)
    rain = Column(Float)
    cloud_cover = Column(Float)
    soil_temperature_7_to_28cm = Column(Float)
    soil_moisture_7_to_28cm = Column(Float) 


def get_engine():
    engine = create_engine(DATABASE_URL, echo=False)
    return engine

def init_db():
    """create tables if they do not exist yet."""
    engine = get_engine()
    Base.metadata.create_all(engine)
    logger.info("Database tables ready.")
    return engine

def parse_response(data: dict, station_id: str) -> pd.DataFrame:
    """
    Flatten the Open-Meteo hourly JSON into a tidy DataFrame.
    Each call to fetch_weather() returns this structure.
    """
    hourly = data["hourly"]
    df = pd.DataFrame({
        "timestamp":           pd.to_datetime(hourly["time"]),
        "station_id":          station_id,
        "temperature_2m":      hourly.get("temperature_2m"),
        "shortwave_radiation":  hourly.get("shortwave_radiation"),
        "windspeed_10m":       hourly.get("wind_speed_10m"),
        "wind_direction_10m": hourly.get("wind_direction_10m"),
        "wind_gusts_10m": hourly.get("wind_gusts_10m"),
        "relative_humidity_2m": hourly.get("relative_humidity_2m"),
        "rain": hourly.get("rain"),
        "cloud_cover": hourly.get("cloud_cover"),
        "soil_temperature_7_to_28cm": hourly.get("soil_temperature_7_to_28cm"),
        "soil_moisture_7_to_28cm": hourly.get("soil_moisture_7_to_28cm"),
    })
    return df

#Save to DB
def save_to_db(df: pd.DataFrame, engine) -> int:
    """
    Insert rows, skipping duplicates (same timestamp + station_id).
    Returns the number of new rows inserted.
    """
    with Session(engine) as session:
        existing = session.execute(
            text("SELECT timestamp, station_id FROM weather_readings")
        ).fetchall()
        existing_keys = {(str(r[0]), r[1]) for r in existing}

        new_rows = [
            WeatherReading(
                timestamp=row.timestamp,
                station_id=row.station_id,
                temperature_2m=row.temperature_2m,
                shortwave_radiation=row.shortwave_radiation,
                windspeed_10m=row.windspeed_10m,
                wind_direction_10m = row.wind_direction_10m,
                wind_gusts_10m = row.wind_gusts_10m,
                relative_humidity_2m= row.relative_humidity_2m,
                rain = row.rain,
                cloud_cover = row.cloud_cover,
                soil_temperature_7_to_28cm = row.soil_temperature_7_to_28cm,
                soil_moisture_7_to_28cm = row.soil_moisture_7_to_28cm,
               
            )
            for row in df.itertuples()
            if (str(row.timestamp), row.station_id) not in existing_keys
        ]

        session.add_all(new_rows)
        session.commit()
        logger.info(f"Inserted {len(new_rows)} new rows.")
        return len(new_rows)
    
# saving backup CSV to data/raw/
def save_raw_backup(df: pd.DataFrame, start_date: str, station_id: str):
    path = f"data/raw/{station_id}_{start_date}.csv"
    df.to_csv(path, index=False)
    logger.info(f"Raw backup saved → {path}")


# Main pipeline
def run_ingestion(start_date: str, end_date: str, station_id: str = "plateau_jos"):
    logger.info(f"Fetching {start_date} → {end_date} for station: {station_id}")

    raw = fetch_weather(start_date, end_date)
    df  = parse_response(raw, station_id)

    save_raw_backup(df, start_date, station_id)

    engine = init_db()
    inserted = save_to_db(df, engine)

    logger.info(f"Pipeline complete. {inserted} rows added to DB.")
    return df


if __name__ == "__main__":
    df = run_ingestion(
        start_date="2024-01-01",
        end_date="2024-01-31",
        station_id="plateau_jos"
    )
    print(df.head(10))
    print(f"\nShape: {df.shape}")