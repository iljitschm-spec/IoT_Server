from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    """Benutzertabelle – hier könnt ihr weitere Felder ergänzen."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)


# TODO: Fügt hier eure eigenen Modelle hinzu
# class Item(Base):
#     __tablename__ = "items"
#     id    = Column(Integer, primary_key=True, index=True)
#     name  = Column(String(100), nullable=False)
#     ...

#Sensoren Klasse
class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)

    # Beziehung: ein Sensor hat viele Werte
    values = relationship("SensorValue", back_populates="sensor")

#Sensoren Werte Klasse
class SensorValue(Base):
    __tablename__ = "sensor_values"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    # Beziehung zurück zum Sensor
    sensor = relationship("Sensor", back_populates="values")
