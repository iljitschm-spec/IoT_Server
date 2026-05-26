# router_historic.py
# Include in main.py:
#   from router_historic import router as historic_router
#   app.include_router(historic_router)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from database import get_db
from models import Sensor, SensorValue
from schemas import SensorHistoricResponse, DataPoint
router = APIRouter(prefix="/sensors", tags=["Historic Data"])


def get_sensor(sensor_id: int, db: Session):
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


def get_aggregated_data(db: Session, sensor_id: int, since: datetime, until: datetime, time_format: str):
    rows = (
        db.query(
            func.date_format(SensorValue.timestamp, time_format).label("time"),
            func.avg(SensorValue.value).label("avg"),
            func.min(SensorValue.value).label("min"),
            func.max(SensorValue.value).label("max"),
        )
        .filter(
            SensorValue.sensor_id == sensor_id,
            SensorValue.timestamp >= since,
            SensorValue.timestamp <= until,
        )
        .group_by("time")
        .order_by("time")
        .all()
    )

    return [
        DataPoint(
            time=row.time,
            avg=round(row.avg, 2),
            min=round(row.min, 2),
            max=round(row.max, 2),
        )
        for row in rows
    ]


# Last 24 hours – one point per hour
@router.get("/{sensor_id}/historic/day", response_model=SensorHistoricResponse)
def historic_day(sensor_id: int, db: Session = Depends(get_db)):
    sensor = get_sensor(sensor_id, db)
    now = datetime.now()
    data = get_aggregated_data(db, sensor_id, since=now - timedelta(hours=24), until=now, time_format="%Y-%m-%d %H:00:00")
    return SensorHistoricResponse(sensor_id=sensor.id, sensor_name=sensor.name, range="day", data=data)


# Last 30 days – one point per day
@router.get("/{sensor_id}/historic/month", response_model=SensorHistoricResponse)
def historic_month(sensor_id: int, db: Session = Depends(get_db)):
    sensor = get_sensor(sensor_id, db)
    now = datetime.now()
    data = get_aggregated_data(db, sensor_id, since=now - timedelta(days=30), until=now, time_format="%Y-%m-%d 00:00:00")
    return SensorHistoricResponse(sensor_id=sensor.id, sensor_name=sensor.name, range="month", data=data)


# Last 12 months – one point per month
@router.get("/{sensor_id}/historic/year", response_model=SensorHistoricResponse)
def historic_year(sensor_id: int, db: Session = Depends(get_db)):
    sensor = get_sensor(sensor_id, db)
    now = datetime.now()
    data = get_aggregated_data(db, sensor_id, since=now - timedelta(days=365), until=now, time_format="%Y-%m-01 00:00:00")
    return SensorHistoricResponse(sensor_id=sensor.id, sensor_name=sensor.name, range="year", data=data)
