<script lang="ts">
    import Button from "$lib/Components/Button.svelte";

    let { loggedIn = $bindable(), showLogIn = $bindable() } = $props();

    let userIsLoggingIn: boolean = $state(true);
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

        if (userIsLoggingIn) {
            //einloggen
            loggedIn = true;
        } else {
            //registrieren
        }

        showLogIn = false;
        userIsLoggingIn = true;
    }

    function closeDialog() {
        showLogIn = false;
    }

    function toggleMode() {
        userIsLoggingIn = !userIsLoggingIn;
    }
</script>

<p>Sie sind noch nicht eingeloggt!</p>

<dialog
        bind:this={dialog}
        onclose={closeDialog}
        onclick={(e) => { if (e.target === dialog) dialog.close(); }}
>
    <form onsubmit={handleSubmit}>
        <p>Username:</p>
        <input type="text" name="username" bind:value={username} />

        <p>Password:</p>
        <input type="password" name="password" bind:value={password} />
        <br>

        <div class="logInButton">
            <Button
                    name={userIsLoggingIn ? "Log In" : "Registrieren"}
                    onclick_function={handleSubmit}
            />
            <Button name="Schließen" onclick_function={closeDialog} />
        </div>

        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
        <p class="toggle-text" onclick={toggleMode}>
            {userIsLoggingIn ? "Noch kein Account? Registrieren" : "Bereits einen Account? Einloggen"}
        </p>
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

    .toggle-text {
        color: var(--accent);
        cursor: pointer;
    }

    .toggle-text:hover {
        text-decoration: underline;
    }
</style>