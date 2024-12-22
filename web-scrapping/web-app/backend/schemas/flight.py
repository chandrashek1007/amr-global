from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FlightMasterBase(BaseModel):
    start_location: str
    end_location: str
    flight_number: str
    departure_date_time: datetime
    arrival_date_time: datetime
    flight_duration: str
    departure_location: str
    arrival_location: str
    price: float
    website: str
    url: Optional[str] = None
    class Config:
        from_attributes = True


class FlightMasterResponse(FlightMasterBase):
    id: int
    created_at: datetime
    updated_at: datetime
    status: str