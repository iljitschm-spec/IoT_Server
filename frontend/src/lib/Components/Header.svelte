<script lang="ts">
    import Button from "$lib/Components/Button.svelte";

    let { loggedIn = $bindable(), showLogIn = $bindable() } = $props();

    let buttonName = $derived(loggedIn ? "Log Out" : "Log In");

    function handleHeaderClick() {
        if (loggedIn) {
            loggedIn = false;
        } else {
            showLogIn = true;
        }
    }
</script>

<header>
    <h1>IOT - Sensor Dashboard</h1>
    <Button name={buttonName} onclick_function={handleHeaderClick} />
</header>

<style>
    header {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: var(--cards);
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin: 0 auto;
        box-sizing: border-box;
        color: var(--text-primary);
    }
    h1 {
        color: var(--text-primary);
        font-size: 2rem;
        text-align: center;
        font-weight: bold;
        margin: auto;
        padding: 0.5rem;
    }
</style>