<script lang="ts">
    import SensorCard from "$lib/Components/SensorCard.svelte";
    import SensorInformation from "./SensorInformation.svelte";
    import { connectMqtt, disconnectMqtt, mqttData } from "../mqttService.svelte.ts";
    import {onMount, onDestroy} from "svelte";
    
    let sensor_list = $derived(Object.values(mqttData.sensors));

    let usedSensor = $derived(sensor_list.find(sensor => sensor.id === selectedId) || sensor_list[0])

    let selectedId: number = $state<number>(0);

    function handleCardClick(sensor: any) {
        usedSensor = sensor;
        console.log(sensor.data)
    }

    $effect(() => {
        if (!selectedId && sensor_list.length > 0) {
            selectedId = sensor_list[0].id;
        }
    });

    onMount(() => {
        connectMqtt("ws://localhost:9001", "sensors/#");
        console.log("Connected");
    })

    onDestroy(() => {
        disconnectMqtt();
        console.log("Disconnected");
    })
</script>

<div class="content-wrapper">
    <ul class="sensor-list">
        {#each sensor_list as sensor }
            <SensorCard sensorName={`Sensor ${sensor.id}`}
                        values={sensor.data} 
                        type={sensor.type} 
                        onclick={() => handleCardClick(sensor)} 
                        online={sensor.online}
                        active={sensor.id === usedSensor.id}
            />
        {/each}
    </ul>
    <div class="content">
        {#if usedSensor}
            <SensorInformation activeSensor={usedSensor} />
        {:else}
            <div class="loading-state">
                <p>Warte auf Sensordaten...</p>
            </div>
        {/if}
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
        height: 80vh;
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
        align-items: center;
        gap: 1rem;
        height: 100%;
        overflow-y: auto;
        overflow-x: hidden;
    }

    * {
        scrollbar-width: thin;
        scrollbar-color: var(--border) transparent;
        ::-webkit-scrollbar{
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track{
            background: transparent;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb{
            background-color: var(--border);
            border-radius: 4px;
        }
        ::webkit-scrollbar-thumb:active{
            background-color: var(--accent);
        }
    }
</style>