<script lang="ts">
	import LogInView from "$lib/Components/LogInView.svelte";
	import Dashboard from "$lib/Components/Dashboard.svelte";
	import Header from "$lib/Components/Header.svelte";

	let loggedIn: boolean = $state(false);
	let showLogIn: boolean = $state(false);
</script>

<main>
	<Header bind:loggedIn bind:showLogIn />
	<br>
	<div class="container">
		{#if loggedIn}
			<Dashboard />
		{:else}
			<div class="notLoggedIn">
				<LogInView bind:loggedIn bind:showLogIn />
			</div>
		{/if}
	</div>
</main>

<style>
	main {
		margin: 0;
		box-sizing: border-box;
		padding: 1rem;
		color: var(--text-primary);
	}

	.container {
		display: flex;
		flex-direction: column;
		flex-wrap: wrap;
		min-height: 75vh;
		max-height: 80vh;

	}

	.notLoggedIn {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
</style>