import time
import random
import json
import paho.mqtt.client as mqtt
from datetime import datetime

sensors = {
    "1": {"id": "1", "name": "Sensor 1", "type": "temperature", "value": 22, "step": 0.3, "min": 18, "max": 28, "active": True},
    "2": {"id": "2", "name": "Sensor 2", "type": "temperature", "value": 24, "step": 0.3, "min": 18, "max": 30, "active": True},
    "3": {"id": "3", "name": "Sensor 3", "type": "humidity",    "value": 60, "step": 1.0, "min": 40, "max": 80, "active": True},
    "4": {"id": "4", "name": "Sensor 4", "type": "temperature", "value": 20, "step": 0.3, "min": 16, "max": 26, "active": True},
    "5": {"id": "5", "name": "Sensor 5", "type": "humidity",    "value": 45, "step": 1.0, "min": 30, "max": 70, "active": True}
}

TOPIC = "commands/+/status" 

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected (rc={rc})")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    topic = msg.topic
    parts = topic.split("/")
    
    if len(parts) != 3 or parts[0] != "commands" or parts[2] != "status":
        return
    
    sensor_id = parts[1]
    
    if sensor_id not in sensors:
        print(f"[MQTT] Unbekannter Sensor: {sensor_id}")
        return
    
    payload = msg.payload.decode("utf-8")
    active = payload == "active"
    
    sensors[sensor_id]["active"] = active
    print(f"-> Sensor {sensor_id} ist jetzt {'aktiv' if active else 'inaktiv'}")
    
    client.publish(f"sensors/{sensor_id}/status", "online" if active else "offline")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883)
client.loop_start()

for s in sensors.values():
    client.publish(f"sensors/{s['id']}/status", "online")

print("Simulator läuft.")

while True:
    for sensor_id, v in sensors.items():
        if not v["active"]:
            continue
        
        v["value"] += random.uniform(-v["step"], v["step"])
        v["value"] = max(v["min"], min(v["max"], v["value"]))
        
        payload = json.dumps({
            "value": round(v["value"], 1),
            "timestamp": datetime.now().isoformat()
        })
        
        client.publish(f"sensors/{v['id']}/{v['type']}", payload)
        print(f"{v['id']} {v['type']}: {round(v['value'], 1)}")
    
    time.sleep(1)