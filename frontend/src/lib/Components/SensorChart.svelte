<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Chart } from 'chart.js/auto';

    let { activeSensor } = $props();
    let canvasElement: HTMLCanvasElement;
    let chartInstance: Chart | null = null;

    onMount(() => {
    chartInstance = new Chart(canvasElement, {
        type: 'line',
        data: {
            labels: activeSensor.data.map((_: any, i: number) => `T-${activeSensor.data.length - i - 1}`),
            datasets: [{
                label: activeSensor.type,
                data: [...activeSensor.data],     // ← der wichtige Trick: Kopie!
                borderColor: 'rgb(255, 252, 192)',
                backgroundColor: 'rgba(255, 192, 203, 0.43)',
                fill: true,
                tension: 0.4
            }]
        }
    });
});

    onDestroy(() => {
        chartInstance?.destroy();
    });

    $effect(() => {
    console.log('Sensor wurde gewechselt zu:', activeSensor.name);
    
    if (!chartInstance) return;  // wenn der char noch nicht erstellt
    
    // dIe neuen labels geenriern
    chartInstance.data.labels = activeSensor.data.map(
        (_: any, i: number) => `T-${activeSensor.data.length - i - 1}`
    );
    
    
    chartInstance.data.datasets[0].data = [...activeSensor.data];
    

    chartInstance.data.datasets[0].label = activeSensor.type;
    

    chartInstance.update();
});
</script>

<div class="chart-container">
    <canvas bind:this={canvasElement}></canvas>
</div>

<style>
    .chart-container {
        position: relative;
        width: 100%;
        height: 100%;
        min-height: 300px;
    }
</style>