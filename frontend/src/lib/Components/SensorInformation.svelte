<script lang="ts">
    import { publishCommand } from "../mqttService.svelte.ts";
    import SensorChart from "./SensorChart.svelte";
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
    <button class="toggle-btn" onclick={toggleSensor}>
        {activeSensor.online === true ? 'Ausschalten' : 'Einschalten'}
    </button>
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
    .toggle-btn {
        padding: 0.5rem 1rem;
        background-color: var(--cards);
        border: 1px solid var(--border);
        color: inherit;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: background-color 0.2s;
        width: fit-content;
    }
    .toggle-btn:hover {
        background-color: var(--accent);
    }
</style>