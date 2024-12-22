from alembic.util import status
from sqlalchemy.orm import Session
from fastapi import Query, Depends, APIRouter, HTTPException
from sqlalchemy import select, and_, func, cast, Date, Time
from typing import List, Optional, Dict
from datetime import datetime, time
from models.notification import NotificationTable
from schemas.notification import NotificationCreate
from utils.database import get_db

router = APIRouter()

def to_dict(instance):
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}


@router.post("/")
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    new_notification = NotificationTable(
        user_id=notification.user_id,
        source=notification.source,
        destination=notification.destination,
        departure_date=notification.departure_date,
        departure_time_range=notification.departure_time_range,
        estimated_price=notification.estimated_price,
        status='Active',
        track_till_date=notification.track_till_date,  # Add new field
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return {"message": "Notification created successfully", "notification": to_dict(new_notification)}



@router.get("/")
def get_notifications(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """
    Retrieve notifications filtered by user_id.

    Args:
        user_id (int, optional): The ID of the user to filter notifications.
        db (Session): Database session.

    Returns:
        List[dict]: A list of notifications for the given user_id or all notifications if no user_id is provided.
    """
    if user_id:
        notifications = db.query(NotificationTable).filter(NotificationTable.user_id == user_id).all()
        if not notifications:
            return {"notifications": []}
    else:
        notifications = db.query(NotificationTable).all()

    return {"notifications": [to_dict(notification) for notification in notifications]}


@router.put("/{notification_id}")
def update_notification(notification_id: int, notification: NotificationCreate, db: Session = Depends(get_db)):
    existing_notification = db.query(NotificationTable).filter(NotificationTable.id == notification_id).first()
    if not existing_notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    for key, value in notification.dict().items():
        setattr(existing_notification, key, value)  # Update fields dynamically

    db.commit()
    db.refresh(existing_notification)
    return {"message": "Notification updated successfully", "notification": to_dict(existing_notification)}


@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(NotificationTable).filter(NotificationTable.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted successfully"}
