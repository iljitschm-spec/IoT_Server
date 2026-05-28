<script>
    let { name, onclick_function, type} = $props();
</script>
    <button onclick={onclick_function} type={type}>
        {name}
    </button>

<style>
    button {
        color: var(--text-primary);
        font-weight: bold;
        display: inline-block;
        text-align: center;
        border: 1px var(--border) solid;
        border-radius: 5px;
        padding: 1rem;
        background-color: var(--accent);
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
    }
    button:hover {
        background-color: var(--hover);
    }
    button:active {
        background-color: var(--hover);
    }

</style>