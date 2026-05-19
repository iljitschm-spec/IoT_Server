<script lang="ts">
    import Button from "$lib/Components/Button.svelte";

    let { loggedIn = $bindable(), showLogIn = $bindable() } = $props();

    let dialog: HTMLDialogElement;
    let username = $state("");
    let password = $state("");

    $effect(() => {
        if (showLogIn && dialog && !dialog.open) {
            dialog.showModal();
        } else if (!showLogIn && dialog && dialog.open) {
            dialog.close();
        }
    });

    function handleSubmit(e?: Event) {
        if (e) e.preventDefault(); // Verhindert das Neuladen der Seite

        loggedIn = true;
        showLogIn = false;
    }

    function closeDialog() {
        showLogIn = false;
    }
</script>

<p>Sie sind noch nicht eingeloggt!</p>

<dialog bind:this={dialog} onclose={closeDialog} onclick={(e) => { if (e.target === dialog) dialog.close(); }}>
    <form onsubmit={handleSubmit}>
        <p>Username:</p>
        <input type="text" name="username" bind:value={username} />

        <p>Password:</p>
        <input type="password" name="password" bind:value={password} />
        <br>
        <div class="logInButton">
            <Button name="Log In" onclick_function={handleSubmit} />
            <Button name="Schließen" onclick_function={closeDialog} />
        </div>
    </form>
</dialog>

<style>
    form {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
    }

    input {
        width: 200px;
        border-radius: 0.4rem;
        height: 1.2rem;
        color: var(--text-primary);
        border: 2px solid var(--border);
        background-color: var(--background);
        padding: 0.2rem 0.5rem;
    }

    dialog {
        max-width: 32em;
        padding: 1.5rem;
        background-color: var(--cards);
        border: 1px solid var(--border);
        border-radius: 1rem;
        color: var(--text-primary);
    }

    dialog::backdrop {
        background: rgba(0, 0, 0, 0.6);
    }
</style>