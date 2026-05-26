import mqtt from "mqtt";

export const mqttData = $state({
    sensors: {} as Record<string, any>
});

let client: mqtt.MqttClient | null = null;

export function connectMqtt(url: string, topic: string) {
    if (client?.connected) {
        return;
    }

    client = mqtt.connect(url);

    client.on("connect", () => {
        client?.subscribe(topic);
    });

    client.on("message", (topic, msg) => {
        const payload = msg.toString();
        const parts = topic.split("/");

        if (parts.length === 3 && parts[0] === "sensors") {
            const id = parts[1];
            const metric = parts[2]; //type

            // fügt Sensor hinzu, falls nicht vorhanden
            if (!mqttData.sensors[id]) {
                mqttData.sensors[id] = { id, name: id, data: [], online: true };
            }

            if (metric === "status") {
                mqttData.sensors[id].online = payload === "online";
            } else if (metric === "temperature" || metric === "humidity") {
                mqttData.sensors[id].type = metric === "temperature" ? "Temperature" : "Humidity";
                //Daten als JSON widergeben
                try {
                    const parsed = JSON.parse(payload);
                    mqttData.sensors[id].data.push(parsed);
                } catch (e) {
                    console.error("Payload ist kein valides JSON:", payload);
                }
            }
        }
    });

    client.on("error", (err) => {
        console.log( `Fehler: ${err.message}`);
        disconnectMqtt();
    });
}

export function publishCommand(sensorId: string, turnOn: boolean) {
    if (client?.connected) {
        // true = online, false = offline
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