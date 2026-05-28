<script lang="ts">
    import Button from "$lib/Components/Button.svelte";
    import {logout} from "$lib/api";

    let { loggedIn = $bindable(), showLogIn = $bindable() } = $props();

    let buttonName = $derived(loggedIn ? "Log Out" : "Log In");

    function handleHeaderClick() {
        if (loggedIn) {
            loggedIn = false;
            logout();
        } else {
            showLogIn = true;
        }
    }
</script>

<header>
    <h1>IOT - Sensor Dashboard</h1>
    <Button name={buttonName} onclick_function={handleHeaderClick} type={"button"} />
</header>

<style>
    header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: var(--cards);
        border: 1px solid var(--border);
        border-radius: 1rem;
        padding: 1rem;
        margin: 0;
        box-sizing: border-box;
        width: 100%;
    }

    h1 {
        color: var(--text-primary);
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0;
    }
</style>