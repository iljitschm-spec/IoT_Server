<script lang="ts">
    let {sensorName, values, type, onclick, online, active} = $props();
</script>


<li>
    <div onclick={onclick} class="card {active === true ? 'active' : ''}">
        <div class="card-body">
            <h3 class={online ===false ? 'offline' : 'online'} >
                {sensorName}
            </h3>
            <p>{type}: {values[values.length - 1]}</p>
        </div>
    </div>
</li>

<style>
    li {
        display: flex;
        flex-direction: column;
        width: 200px;
        flex-grow: 1;
        min-height: 100px;
    }

    .card {
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        text-align: center;
        cursor: pointer;
        flex-grow: 1;

        color: var(--text-primary);
        background-color: var(--cards);
        border: 1px solid var(--border);
        border-radius: 1rem;
    }

    .active {
        border: 1px solid var(--accent);
    }

    .offline {
        color: var(--red)
    }
</style>