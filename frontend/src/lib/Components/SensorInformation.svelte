<script lang="ts">
    let { activeSensor } = $props();
    let time: number = $state(11)
</script>
<div class="content-wrapper">
    <h2>{activeSensor.name}</h2>
    <p>Status: 
        <span style="color: {activeSensor.online === true ? 'var(--green)' : 'var(--red)'}">
            {activeSensor.online === true ? 'Online' : 'Offline'}
        </span>
    </p>
    <br>
    <div class="table-container">
        <table>
            <tbody>
            <tr>
                <th>Zeit</th>
                <th>Wert</th>
            </tr>
            {#each activeSensor.data as value}
                <tr>
                    <td>{time.toString()+':00'}</td>
                    <td>{value}{activeSensor.type === 'Temperature' ? '°C' : '%'}</td>
                </tr>
            {/each}
            </tbody>
        </table>
    </div>
</div>

<style>
    .content-wrapper {
        display: flex;
        flex-direction: column;
        height: 100%;
        max-height: 450px;
    }
    .table-container {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        overflow-y: auto;
    }
    table {
        width: 50%;
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        border-collapse: collapse;
    }
    th, td {
        padding: 0.5rem;
        text-align: center;
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        border-collapse: collapse;
    }
    th {
        position: sticky;
        top: 0;
        background-color: var(--cards);
        z-index: 1;
        font-weight: bold;
    }
    * {
        scrollbar-width: thin;
        scrollbar-color: var(--border) transparent;
        ::-webkit-scrollbar{
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track{
            background: transparent;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb{
            background-color: var(--border);
            border-radius: 4px;
        }
        ::webkit-scrollbar-thumb:active{
            background-color: var(--accent);        
        }
    }
</style>