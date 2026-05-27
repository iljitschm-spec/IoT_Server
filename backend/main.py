from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from router_historic import router as historic_router
from mqtt_subscriber import start_mqtt
from auth import (
    DUMMY_HASH,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from database import Base, engine, get_db
import models
from schemas import Token, UserRegister, UserResponse, SensorCreate, SensorResponse, SensorValueCreate, SensorValueResponse

# Tabellen anlegen (falls noch nicht vorhanden)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mein Projekt", version="0.1.0")
app.include_router(historic_router)
from mqtt_subscriber import start_mqtt
mqtt_client = None
@app.on_event("startup")
def _startup():
    global mqtt_client 
    mqtt_client = start_mqtt()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ], # Erlaubt deinem Svelte-Frontend den Zugriff
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Authentifizierung
# ---------------------------------------------------------------------------

@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):

    # 1. prüfen ob user existiert
    existing_user = db.query(models.User).filter(
        (models.User.username == data.username) |
        (models.User.email == data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User existiert bereits")

    # 2. Passwort hashen
    hashed_password = get_password_hash(data.password)

    # 3. User speichern
    user = models.User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):

    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    # Timing Schutz
    if not user:
        verify_password(form_data.password, DUMMY_HASH)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Benutzername oder Passwort falsch",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": create_access_token(user.username),
        "token_type": "bearer",
    }


@app.get("/my-profile", response_model=UserResponse)
def get_profile(
    current_username: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):

    user = db.query(models.User).filter(
        models.User.username == current_username
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User nicht gefunden")

    return user


# ---------------------------------------------------------------------------
# TODO: Eure eigenen Endpoints hier einfügen
# ---------------------------------------------------------------------------

# Beispiel:
# @app.get("/items")
# def get_items(db: Session = Depends(get_db)):
#     return db.query(Item).all()
#
# @app.post("/items", status_code=201)
# def create_item(data: ItemCreate, db: Session = Depends(get_db)):
#     item = Item(**data.model_dump())
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     return item

@app.get("/sensors", response_model=list[SensorResponse])
def get_sensors(db: Session = Depends(get_db)):
    return db.query(models.Sensor).all()



@app.post("/sensors", response_model=SensorResponse)
def create_sensor(data: SensorCreate, db: Session = Depends(get_db)):
    sensor = models.Sensor(**data.dict())
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor

@app.post("/sensor/{sensor_id}/values", response_model=SensorValueResponse)
def create_sensor_value(sensor_id: int, data: SensorValueCreate, db: Session = Depends(get_db)):
    value = models.SensorValue(
        sensor_id=sensor_id,
        value=data.value
    )
    db.add(value)
    db.commit()
    db.refresh(value)
    return value

@app.get("/sensor/{sensor_id}/values", response_model=list[SensorValueResponse])
def get_sensor_values(sensor_id: int, db: Session = Depends(get_db)):
    return db.query(models.SensorValue)\
             .filter(models.SensorValue.sensor_id == sensor_id)\
             .all()



@app.post("/sensor/{sensor_id}/status?{}")
def change_stauts():
    pass
