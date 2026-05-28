<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Chart } from 'chart.js/auto';
    import { fetchPublic } from '$lib/api';
    import ActionButton from './ActionButton.svelte';

    let { activeSensor } = $props();
    let canvasElement: HTMLCanvasElement;
    let chartInstance: Chart | null = null;

    let horizon = $state("hour");

    function changeHorizon(h: string) {
        horizon = h;
        loadHistoricData(activeSensor);
    }

    async function loadHistoricData(sensor) {
        if (!chartInstance) return;

        try {
            const json = await fetchPublic<any>(`/sensors/${sensor.id}/historic/${horizon}`);
            const historicPoints = json.data || [];

            console.log(`Erhaltene historische Daten (${horizon}):`, historicPoints);

            if (historicPoints.length === 0) {
                console.warn(`Keine historischen Daten für Sensor ${sensor.id} vorhanden.`);
            }

            // Dynamische Formatierung je nach Horizont
            const labels = historicPoints.map((point: any) => {
                // Das Backend nutzt für 'day/month/year' Leerzeichen statt T. 
                // Wir ersetzen es, damit JavaScript das Datum im Safari/Firefox sauber parst.
                const formattedString = point.time.replace(" ", "T");
                const date = new Date(formattedString + "Z"); 
                
                if (isNaN(date.getTime())) return point.time;
                
                // X-Achse je nach ausgewähltem Horizont formatieren
                if (horizon === "hour") {
                    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); 
                } else if (horizon === "day") {
                    return date.toLocaleTimeString([], { hour: '2-digit' }); 
                } else if (horizon === "month") {
                    return date.toLocaleDateString([], { day: '2-digit', month: '2-digit' }); 
                } else {
                    return date.toLocaleDateString([], { month: 'short', year: '2-digit' }); 
                }
            });

            const values = historicPoints.map((point: any) => point.avg);

            chartInstance.data.labels = labels;
            chartInstance.data.datasets[0].data = values;
            chartInstance.data.datasets[0].label = sensor.type;
            
            chartInstance.update();
        } catch (error) {
            console.error("Fehler beim Laden der historischen Daten:", error);
        }
    }

    onMount(() => {
        loadHistoricData(activeSensor);
        chartInstance = new Chart(canvasElement, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: activeSensor.type,
                    data: [],
                    borderColor: '#0EA5E9',
                    tension: 0.4,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, 
                scales: {
                    x: { boundaryGap: false }
                },
            plugins: {
                legend: {
                    display: false },
            }
    }});

        
    });

    onDestroy(() => {
        chartInstance?.destroy();
    });

    $effect(() => {
        if (activeSensor && chartInstance) {
            loadHistoricData(activeSensor);
        }
    });
</script>

<div class="button_wrapper">
    <ActionButton name="Stunde" onclick_function={() => changeHorizon("hour")} active_condition={horizon === "hour"} />
    <ActionButton name="Tag" onclick_function={() => changeHorizon("day")} active_condition={horizon === "day"} />
    <ActionButton name="Monat" onclick_function={() => changeHorizon("month")} active_condition={horizon === "month"} />
    <ActionButton name="Jahr" onclick_function={() => changeHorizon("year")} active_condition={horizon === "year"} />
</div>

<div class="chart-container">
    <canvas bind:this={canvasElement}></canvas>
</div>

<style>
    .button_wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        width: 100%;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }
    .chart-container {
        position: relative;
        width: 100%;
        height: 95%;
        min-height: 300px;
    }
</style>