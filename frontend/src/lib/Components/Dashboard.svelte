<script>
    import SensorCard from "$lib/Components/SensorCard.svelte";


    let sensor_list = [
        {"name": "Sensor 1", "data": {"Temp": 20}},
        {"name": "Sensor 2", "data": {"Temp": 20}},
        {"name": "Sensor 3", "data": {"Humid": 50}},
        {"name": "Sensor 4", "data": {"Humid": 50}},
        {"name": "Sensor 5", "data": {"Humid": 50}},
    ]
</script>

<div class="content-wrapper">
    <ul class="sensor-list">
        {#each sensor_list as sensor }
            <SensorCard sensor={sensor.name} values={sensor.data} />
        {/each}
    </ul>
    <div class="content">
        asdf
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
        align-items: center;
        justify-content: center;
        background-color: var(--cards);
        border: 1px solid var(--border);
        border-radius: 1rem;
        text-align: center;
        flex-grow: 1;
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