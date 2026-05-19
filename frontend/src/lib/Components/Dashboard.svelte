<script lang="ts">
    import SensorCard from "$lib/Components/SensorCard.svelte";
    import SensorInformation from "./SensorInformation.svelte";


    let sensor_list = [
        {"name": "Sensor 1", "type": "Temperature", "data": [20, 21, 22, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], "online": true},
        {"name": "Sensor 2", "type": "Temperature", "data": [20, 24, 23], "online": true},
        {"name": "Sensor 3", "type": "Humidity", "data": [50, 55, 53], "online": false},
        {"name": "Sensor 4", "type": "Humidity", "data": [50, 49, 47], "online": true},
        {"name": "Sensor 5", "type": "Humidity", "data": [50, 51, 52], "online": true},
    ]

    let usedSensor = $state(sensor_list[0]);

    function handleCardClick(sensor: any) {
        usedSensor = sensor;
    }
</script>

<div class="content-wrapper">
    <ul class="sensor-list">
        {#each sensor_list as sensor }
            <SensorCard sensorName={sensor.name} 
                        values={sensor.data} 
                        type={sensor.type} 
                        onclick={() => handleCardClick(sensor)} 
                        online={sensor.online} />
        {/each}
    </ul>
    <div class="content">
        <SensorInformation activeSensor={usedSensor} />
    </div>

</div>


<style>
    .content-wrapper{
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 1.5rem;
        width: 100%;
        margin: 0 auto;
    }

    .content{
        display: flex;
        flex-direction: column;
        background-color: var(--cards);
        border: 1px solid var(--border);
        border-radius: 1rem;
        flex-grow: 1;
        padding: 1rem;
    }

    .sensor-list {
        list-style-type: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
        justify-content: center; 
        gap: 1.5rem;
    }
</style>