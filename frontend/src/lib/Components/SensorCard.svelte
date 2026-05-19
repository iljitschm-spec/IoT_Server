<script lang="ts">
    let {sensorName, values, type, onclick, online} = $props();
</script>


<li>
    <button type="button" onclick={onclick} class="card">
        <div class="card-body">
            <h3 class={online ===false ? 'offline' : 'online'} >
                {sensorName}
            </h3>
            <p>{type}: {values[values.length - 1]}</p>
        </div>
    </button>
</li>

<style>
    .card {
        appearance: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: var(--cards);
        border: 1px solid var(--border);
        border-radius: 1rem;
        width: 200px;
        text-align: center;
        cursor: pointer;
        color: var(--text-primary);
    }

    .card:focus-visible {
        outline: 2px solid Highlight;
        outline-offset: 2px;
    }
    
    .offline {
        color: var(--red)
    }
</style>