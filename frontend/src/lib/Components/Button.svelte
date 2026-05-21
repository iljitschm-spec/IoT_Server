<script>
    let { name, onclick_function} = $props();
</script>

    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    <div onclick={onclick_function}>
        {name}
    </div>

<style>
    div {
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
    div:hover {
        background-color: var(--hover);
    }
    div:active {
        background-color: var(--hover);
    }

</style>