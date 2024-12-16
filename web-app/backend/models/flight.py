from sqlalchemy import Column, Integer, String, DateTime, Double
from utils.database import Base

class FlightMaster(Base):
    __tablename__ = "flights_master"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    start_location = Column(String, nullable=False)
    end_location = Column(String, nullable=False)
    flight_number = Column(String, nullable=False)
    departure_date_time = Column(DateTime, nullable=False)
    arrival_date_time = Column(DateTime, nullable=False)
    flight_duration = Column(String, nullable=False)
    departure_location = Column(String, nullable=False)
    arrival_location = Column(String, nullable=False)
    price = Column(Double, nullable=False)
    website = Column(String, nullable=False)
    url = Column(String, nullable=True)



