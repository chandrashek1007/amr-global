# from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
# from utils.database import Base
#
# class FlightUserMapping(Base):
#     __tablename__ = "flights_user_mapping"
#     id = Column(Integer, primary_key=True, index=True)
#     created_at = Column(DateTime, nullable=False)
#     updated_at = Column(DateTime, nullable=False)
#     flight_master_id = Column(String, ForeignKey('flights_master.id'), nullable=False)
#     user_id = Column(String, ForeignKey('users.id'), nullable=False)
#     current_flight_price = Column(Float, nullable=False)
#     updated_flight_price = Column(Float, nullable=False)
#     notification_sent = Column(String, nullable=False)
#     last_notification_time = Column(DateTime, nullable=False)

