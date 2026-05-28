<script lang="ts">
    import { publishCommand } from "../mqttService.svelte.ts";
    import SensorChart from "./SensorChart.svelte";
    import  ActionButton  from "./ActionButton.svelte";
    let { activeSensor } = $props();
    function toggleSensor() {
        publishCommand(activeSensor.id, !activeSensor.online);
    }
</script>

<div class="content-wrapper">
    <h2>
        {`Sensor ${activeSensor.id}`}
        <span style="color: {activeSensor.online === true ? 'var(--green)' : 'var(--red)'}">● {activeSensor.online === true ? 'Online' : 'Offline'}</span>
    </h2>
    <ActionButton name={activeSensor.online === true ? 'Ausschalten' : 'Einschalten'} onclick_function={toggleSensor} />
    <div class="chart-wrapper">
        <SensorChart {activeSensor} />
    </div>
</div>

<style>
    .content-wrapper {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .chart-wrapper {
        flex-grow: 1;
        min-height: 300px;
        width: 100%;
        padding: 1rem 0;
    }
</style>