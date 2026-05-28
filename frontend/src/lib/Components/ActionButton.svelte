<script>
    let { name, onclick_function, active_condition} = $props();
</script>
    <button onclick={onclick_function} type="button" class="{active_condition ? 'active' : ''}">
        {name}
    </button>

<style>
    button {
        padding: 0.5rem 1rem;
        background-color: var(--cards);
        border: 1px solid var(--border);
        color: inherit;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: background-color 0.2s;
        width: fit-content;
    }
    button:hover {
        background-color: var(--accent);
    }

    .active {
        background-color: var(--accent);
    }

</style>