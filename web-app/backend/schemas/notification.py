from pydantic import BaseModel
from datetime import date

class NotificationCreate(BaseModel):
    user_id: int
    source: str
    destination: str
    departure_date: date
    departure_time_range: str
    estimated_price: float
    track_till_date: date  # New field
