<script lang="ts">
    import Button from "$lib/Components/Button.svelte";
    import { login, register } from "$lib/api";

    let { loggedIn = $bindable(), showLogIn = $bindable() } = $props();

    let userIsLoggingIn: boolean = $state(true);
    let dialog: HTMLDialogElement;
    let username = $state("");
    let password = $state("");
    let email = $state("");
    
    let errorMessage = $state(""); 
    let isLoading = $state(false);

    $effect(() => {
        if (showLogIn && dialog && !dialog.open) {
            if (!isLoading) {
                username = "";
                password = "";
                email = "";
                errorMessage = ""; 
            }
            dialog.showModal();
        } else if (!showLogIn && dialog && dialog.open) {
            dialog.close();
        }
    });

    async function handleSubmit(e?: Event) {
        if (e) e.preventDefault();

        isLoading = true;
        errorMessage = "";

        if (!username || !password || (!userIsLoggingIn && !email)) {
            errorMessage = "Bitte fülle alle erforderlichen Felder aus.";
            isLoading = false;
            return;
        }

        if (userIsLoggingIn) {
            try {
                await login(username, password);
                loggedIn = true;
                showLogIn = false;
                userIsLoggingIn = true;
            } catch (error: any) {
                errorMessage = error.message || "Login fehlgeschlagen. Bitte überprüfe deine Daten.";
            } finally {
                isLoading = false;
            }
        } else {
            try {
                await register(username, email, password);
                await login(username, password);

                loggedIn = true;
                showLogIn = false;
                userIsLoggingIn = true;

            } catch (error: any) {
                errorMessage = error.message || "Registrierung fehlgeschlagen. Möglicherweise ist der Benutzername bereits vergeben.";
            } finally {
                isLoading = false;
            }
        }
    }

    function closeDialog() {
        if (!isLoading) {
            showLogIn = false;
        }
    }

    function toggleMode() {
        userIsLoggingIn = !userIsLoggingIn;
        errorMessage = "";
    }

</script>

{#if !loggedIn}
    <p>Sie sind noch nicht eingeloggt!</p>
{/if}

<dialog
        bind:this={dialog}
        onclose={closeDialog}
        onclick={(e) => { if (e.target === dialog && !isLoading) dialog.close(); }}
>
    <form onsubmit={handleSubmit}>

        <label for="username">Benutzername:</label>
        <input type="text" id="username" name="username" bind:value={username} />
        
        {#if !userIsLoggingIn}
            <label for="email">E-Mail:</label>
            <input type="email" id="email" name="email" bind:value={email} disabled={isLoading} required />
        {/if}
        
        <label for="password">Passwort:</label>
        <input type="password" id="password" name="password" bind:value={password} />
        
        {#if errorMessage}
            <p class="error-message">{errorMessage}</p>
        {/if}
        
        <br>
        
        <div class="logInButton">
            <Button
                    name={userIsLoggingIn ? "Log In" : "Registrieren"}
                    onclick_function={handleSubmit}
            />
            <Button name="Schließen" type="button" onclick_function={closeDialog} />
        </div>
        
        <button type="button" class="toggle-text" onclick={toggleMode}>
            {userIsLoggingIn ? "Noch kein Account? Registrieren" : "Bereits einen Account? Einloggen"}
        </button>
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

    label {
        margin-top: 0.2rem;
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
        transition: 0.5s;
    }

    dialog::backdrop {
        background: rgba(0, 0, 0, 0.6);
    }

    .toggle-text {
        color: var(--accent);
        cursor: pointer;
        margin-top: 0.5rem;
        background: none;
        border: none;
    }

    .toggle-text:hover {
        text-decoration: underline;
    }

    .error-message {
        color: var(--red);
        font-size: 0.85rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
        max-width: 220px;
        line-height: 1.2;
    }
</style>