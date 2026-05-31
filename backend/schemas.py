from datetime import datetime
from pydantic import BaseModel
from typing import Literal


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str

class SensorCreate(BaseModel):
    name: str
    type: str

class SensorResponse(BaseModel):
    id: int
    name: str
    type: str

    model_config = {"from_attributes": True}


class SensorValueCreate(BaseModel):
    value: float


class SensorValueResponse(BaseModel):
    id: int
    value: float
    timestamp: datetime

    model_config = {"from_attributes": True}


class DataPoint(BaseModel):
    time: datetime
    avg: float
    min: float
    max: float


class SensorHistoricResponse(BaseModel):
    sensor_id: int
    sensor_name: str
    range: Literal["hour", "day", "month", "year"]
    data: list[DataPoint]

