from sqlalchemy import Column, Integer, String, Float, Date
from utils.database import Base


class NotificationTable(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    status = Column(String, nullable=True, default='Active')
    departure_date = Column(Date, nullable=False)
    departure_time_range = Column(String, nullable=False)
    estimated_price = Column(Float, nullable=False)
    track_till_date = Column(Date, nullable=False)  # New field
