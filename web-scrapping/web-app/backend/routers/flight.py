from sqlalchemy.orm import Session
from fastapi import Query, Depends, APIRouter, HTTPException
from sqlalchemy import select, and_, func, cast, Date, Time
from typing import List, Optional, Dict
from datetime import datetime, time
from models.flight import FlightMaster
from schemas.flight import FlightMasterResponse
from utils.database import get_db

router = APIRouter()

# Mapping of time range strings to actual time ranges
TIME_RANGES = {
    "6AM-12PM": (time(6, 0), time(12, 0)),
    "12PM-18PM": (time(12, 0), time(18, 0)),
    "18PM-24AM": (time(18, 0), time(23, 59, 59)),
    "0AM-6AM": (time(0, 0), time(6, 0)),
}


@router.get("/", response_model=Dict[str, List[FlightMasterResponse]])
async def get_flights(
    departure_range: Optional[str] = Query(None, description="Departure time range (e.g., '6AM-12PM')"),
    arrival_range: Optional[str] = Query(None, description="Arrival time range (e.g., '6AM-12PM')"),
    departure_location: Optional[str] = Query(None),
    arrival_location: Optional[str] = Query(None),
    departure_date: Optional[datetime] = Query(None, description="Departure date for filtering (YYYY-MM-DD)"),
    arrival_date: Optional[datetime] = Query(None, description="Arrival date for filtering (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    # Validate the time range strings
    if departure_range and departure_range not in TIME_RANGES:
        raise HTTPException(
            status_code=400,
            detail="Invalid departure time range. Valid options are: 6AM-12PM, 12PM-18PM, 18PM-24AM, 0AM-6AM",
        )
    if arrival_range and arrival_range not in TIME_RANGES:
        raise HTTPException(
            status_code=400,
            detail="Invalid arrival time range. Valid options are: 6AM-12PM, 12PM-18PM, 18PM-24AM, 0AM-6AM",
        )

    # Query for departure flights
    departure_conditions = []
    if departure_location:
        departure_conditions.append(FlightMaster.start_location == departure_location)
    if arrival_location:
        departure_conditions.append(FlightMaster.end_location == arrival_location)
    if departure_date:
        departure_conditions.append(cast(FlightMaster.departure_date_time, Date) == departure_date)
    if departure_range:
        dep_start_time, dep_end_time = TIME_RANGES[departure_range]
        departure_conditions.append(
            and_(
                cast(FlightMaster.departure_date_time, Time) >= dep_start_time,
                cast(FlightMaster.departure_date_time, Time) <= dep_end_time,
            )
        )
    departure_query = select(FlightMaster)
    if departure_conditions:
        departure_query = departure_query.where(and_(*departure_conditions))
    departure_result = db.execute(departure_query)
    departure_flights = departure_result.scalars().all()

    # Query for arrival flights (reverse conditions)
    arrival_conditions = []
    if arrival_location:  # Reverse
        arrival_conditions.append(FlightMaster.start_location == arrival_location)
    if departure_location:  # Reverse
        arrival_conditions.append(FlightMaster.end_location == departure_location)
    if arrival_date:
        departure_conditions.append(cast(FlightMaster.departure_date_time, Date) == arrival_date)
    if arrival_range:
        arr_start_time, arr_end_time = TIME_RANGES[arrival_range]
        arrival_conditions.append(
            and_(
                cast(FlightMaster.departure_date_time, Time) >= arr_start_time,
                cast(FlightMaster.departure_date_time, Time) <= arr_end_time,
            )
        )
    arrival_query = select(FlightMaster)
    if arrival_conditions:
        arrival_query = arrival_query.where(and_(*arrival_conditions))
    arrival_result = db.execute(arrival_query)
    arrival_flights = arrival_result.scalars().all()

    # Sort by departure_date_time (ascending) and price (descending)
    departure_response = [
                             FlightMasterResponse.model_validate(flight)
                             for flight in sorted(
            departure_flights, key=lambda x: (x.departure_date_time, -x.price)
        )
                         ][:10]

    arrival_response = [
                           FlightMasterResponse.model_validate(flight)
                           for flight in sorted(
            arrival_flights, key=lambda x: (x.departure_date_time, -x.price)
        )
                       ][:10]

    # Return response as separate objects
    return {
        "departure": departure_response,
        "arrival": arrival_response,
    }
