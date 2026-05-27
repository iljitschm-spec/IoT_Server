<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Chart } from 'chart.js/auto';
    import { fetchPublic } from '$lib/api';

    let { activeSensor } = $props();
    let canvasElement: HTMLCanvasElement;
    let chartInstance: Chart | null = null;

    let horizon = $state("hour"); // Bleibt englisch für die API

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

        loadHistoricData(activeSensor);
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
    <button class="toggle-btn" class:active={horizon === 'hour'} onclick={() => changeHorizon("hour")}>Stunde</button>
    <button class="toggle-btn" class:active={horizon === 'day'} onclick={() => changeHorizon("day")}>Tag</button>
    <button class="toggle-btn" class:active={horizon === 'month'} onclick={() => changeHorizon("month")}>Monat</button>
    <button class="toggle-btn" class:active={horizon === 'year'} onclick={() => changeHorizon("year")}>Jahr</button>
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

    .toggle-btn {
        padding: 0.5rem 1rem;
        background-color: var(--cards);
        border: 1px solid var(--border);
        color: inherit;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.2s;
        width: fit-content;
    }
    .toggle-btn:hover, .toggle-btn.active {
        background-color: var(--accent);
        border-color: var(--accent);
    }
</style>