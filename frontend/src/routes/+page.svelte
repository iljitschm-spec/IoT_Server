<script lang="ts">
	import LogInView from "$lib/Components/LogInView.svelte";
	import Dashboard from "$lib/Components/Dashboard.svelte";
	import Header from "$lib/Components/Header.svelte";
	import {onMount} from "svelte";
	import {isLoggedIn} from "$lib/api";

	let loggedIn: boolean = $state(false);
	let showLogIn: boolean = $state(false);

	//Verhindert das Anzeigen von <LogInView> falls ein Token vorhanden ist.
	let isAppLoading: boolean = $state(true);

	onMount(() => {
		if (isLoggedIn()) {
			loggedIn = true;
		}
		isAppLoading = false;
	})

</script>

<div class="main">
	<Header bind:loggedIn bind:showLogIn />
	<div class="container">
		{#if isAppLoading}
			<div class="loading-state">
			</div>
		{:else if loggedIn}
			<Dashboard />
		{:else}
			<div class="notLoggedIn">
				<LogInView bind:loggedIn bind:showLogIn />
			</div>
		{/if}
	</div>
</div>

<style>
	.main {
		max-width: 100%;
		max-height: 100%;
		width: 100%;
		margin: 0 auto;
		box-sizing: border-box;
		padding: 1rem;
		color: var(--text-primary);

		display: flex;
		flex-direction: column;
		gap: 1.2rem;
	}

	.container {
		display: flex;
		flex-direction: column;
		width: 100%;
	}

	.notLoggedIn {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	.loading-state {
		min-height: 200px;
	}
</style>