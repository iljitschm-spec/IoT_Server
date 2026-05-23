from pydantic import BaseModel
from datetime import datetime


# --- Auth-Schemas ---

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


# TODO: Fügt hier eure eigenen Schemas hinzu
# class ItemCreate(BaseModel):
#     name: str
#     price: int
#
# class ItemResponse(BaseModel):
#     id: int
#     name: str
#     price: int
#     model_config = {"from_attributes": True}

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

