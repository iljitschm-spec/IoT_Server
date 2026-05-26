import json
import paho.mqtt.client as mqtt
from datetime import datetime

from database import SessionLocal
from models import Sensor, SensorValue
import os

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC     = "sensors/#"  


def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected (rc={rc})")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):

    topic = msg.topic                       
    parts = topic.split("/")

    sensor_id_str = parts[1]

    try:
        sensor_id = int(sensor_id_str)
    except ValueError:
        print(f"[MQTT] Invalid sensor_id in topic: {topic}")
        return

    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        value = float(payload["value"])
        timestamp = datetime.fromisoformat(payload["timestamp"])
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"[MQTT] Bad payload on {topic}: {e}")
        return


    db = SessionLocal()
    try:

        sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
        if not sensor:
            sensor = Sensor(id=sensor_id, name=f"Sensor {sensor_id}", type="unknown")
            db.add(sensor)
            db.commit()

        db.add(SensorValue(
            sensor_id=sensor_id,
            value=value,
            timestamp=timestamp,
        ))
        db.commit()
        print(f"[DB] Saved: sensor {sensor_id} → {value}")

    except Exception as e:
        db.rollback()
        print(f"[DB] Error: {e}")
    finally:
        db.close()


def start_mqtt():
    client = mqtt.Client(client_id="db-subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT)
    client.loop_start()  
    return client
