<script lang="ts">
    import Button from "$lib/Components/Button.svelte";
    import {logout} from "$lib/api";
    import {onMount} from "svelte";

    let { loggedIn = $bindable(), showLogIn = $bindable() } = $props();

    let buttonName = $derived(loggedIn ? "Log Out" : "Log In");
    let isDark = $state(true);

    onMount(() => {
        if (localStorage.getItem("theme") === "light") {
            isDark = false;
            document.documentElement.setAttribute("data-theme", "light");
        }
    });

    function toggleTheme() {
        isDark = !isDark;
        if (isDark) {
            document.documentElement.removeAttribute("data-theme");
            localStorage.setItem("theme", "dark");
        } else {
            document.documentElement.setAttribute("data-theme", "light");
            localStorage.setItem("theme", "light");
        }
    }

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
    <div class="actions">
        <button class="theme-toggle" onclick={toggleTheme} aria-label="Theme wechseln">
            {isDark ? "☀️" : "🌒"}
        </button>
        <Button name={buttonName} onclick_function={handleHeaderClick} type={"button"} />
    </div>
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
    .actions {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .theme-toggle {
        background-color: var(--background);
        border: 1px solid var(--border);
        color: var(--text-primary);
        font-size: 1.2rem;
        width: 2.8rem;
        height: 2.8rem;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .theme-toggle:hover {
        background-color: var(--border);
    }
</style>