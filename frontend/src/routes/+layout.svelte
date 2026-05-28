<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
    :global(:root) {
        --background: #0F172A;
        --cards: #1E293B;

        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;

        --accent: #0EA5E9;
        --hover: #38BDF8;
        --click: #7DD3FC;

        --border: #334155;
        --red: #EF4444;
        --green: #10B981;
        --warning: #F59E0B;
        font-family: "Roboto", "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }

    :global([data-theme="light"]) {
        --background: #F1F5F9;
        --cards: #FFFFFF;

        --text-primary: #0F172A;
        --text-secondary: #475569;

        --accent: #0284C7;
        --hover: #0369A1;
        --click: #075985;

        --border: #CBD5E1;
        --red: #DC2626;
        --green: #059669;
        --warning: #D97706;
    }

    :global(body) {
        background-color: var(--background);
        color: var(--text-primary);
        transition: background-color 0.3s ease, color 0.3s ease;
        margin: 0;
    }
</style>

<slot />