import mqtt from "mqtt";

export const mqttData = $state({
    sensors: {} as Record<string, any>
});

let client: mqtt.MqttClient | null = null;

export function connectMqtt() {
    //verbindet sich mit dem MQTT-Broker und abonniert die Themen sensor/# und alerts/#
    if (client?.connected) {
        return;
    }

    client = mqtt.connect("ws://localhost:9001");

    client.on("connect", () => {
        client?.subscribe("sensors/#");
        client?.subscribe("alerts/#");
    });

    client.on("message", (topic, msg) => {
        const payload = msg.toString();
        const parts = topic.split("/");

        //Fall: Unter sensors/# hat sich etwas verändert
        if (parts.length === 3 && parts[0] === "sensors") {
            const id = parts[1];
            const metric = parts[2];

            initSensorIfNeeded(id);

            if (metric === "status") {
                mqttData.sensors[id].online = payload === "online";
            } else if (metric === "temperature" || metric === "humidity") {
                mqttData.sensors[id].type = metric === "temperature" ? "Temperature" : "Humidity";
                try {
                    mqttData.sensors[id].data = JSON.parse(payload);
                } catch (e) {
                    console.error("Payload ist kein valides JSON:", payload);
                }
            }
        }

        //Fall: Unter alerts/# hat sich etwas verändert
        if (parts.length === 2 && parts[0] === "alerts") {
            const id = parts[1];
            initSensorIfNeeded(id);
            mqttData.sensors[id].alert = payload === "true";
        }
    });

    client.on("error", (err) => {
        console.log(`Fehler: ${err.message}`);
        disconnectMqtt();
    });
}

function initSensorIfNeeded(id: string) {
    if (!mqttData.sensors[id]) {
        mqttData.sensors[id] = { id, name: id, data: null, online: true, alert: false, lastSeen: Date.now() };
    } else {
        mqttData.sensors[id].lastSeen = Date.now();
    }

}

export function publishCommand(sensorId: string, turnOn: boolean) {
    if (client?.connected) {
        console.log(sensorId);
        client.publish(`commands/${sensorId}/status`, turnOn ? "active" : "inactive");
    }
}

export function disconnectMqtt() {
    if (client) {
        client.end();
        client = null;
    }
}