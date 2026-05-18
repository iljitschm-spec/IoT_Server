<script lang="ts">
    let {sensor, values} = $props();
</script>


<li>
    <div class="card">
        <div class="card-body">
            <h3>
                {sensor}
            </h3>
            {#each Object.entries(values) as [key, value]}
                <p>{key}: {value}</p>
            {/each}
        </div>
    </div>
</li>

<style>
    .card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: var(--cards);
        border: 1px solid var(--border);
        border-radius: 1rem;
        width: 200px;
        text-align: center;
    }
</style>