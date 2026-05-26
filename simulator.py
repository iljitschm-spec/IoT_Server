import time
import random
import json
import paho.mqtt.client as mqtt
from datetime import datetime

client = mqtt.Client()
client.connect("localhost", 1883)

sensors = [
    {"id": "sensor-1", "type": "temperature", "value": 22, "step": 0.3, "min": 18, "max": 28},
    {"id": "sensor-2", "type": "temperature", "value": 24, "step": 0.3, "min": 18, "max": 30},
    {"id": "sensor-3", "type": "humidity",    "value": 60, "step": 1.0, "min": 40, "max": 80},
    {"id": "sensor-4", "type": "temperature", "value": 20, "step": 0.3, "min": 16, "max": 26},
    {"id": "sensor-5", "type": "humidity",    "value": 45, "step": 1.0, "min": 30, "max": 70},
]

while True:
    for s in sensors:
        s["value"] += random.uniform(-s["step"], s["step"])

        # falls's rausläuft, an die Grenze klemmen
        s["value"] = max(s["min"], min(s["max"], s["value"]))

        payload = json.dumps({
            "value": round(s["value"], 1),
            "timestamp": datetime.now().isoformat()
        })

        client.publish(f"sensors/{s['id']}/{s['type']}", payload)
        print(f"{s['id']} {s['type']}: {round(s['value'], 1)}")

    time.sleep(1)