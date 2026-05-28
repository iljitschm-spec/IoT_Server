/** Basis-URL des FastAPI-Backends */
const API_BASE = 'http://localhost:8000';

/** Hilfsfunktion: gibt den gespeicherten JWT zurück (oder null) */
function getToken(): string | null {
	return localStorage.getItem('token');
}

/** Hilfsfunktion: speichert den JWT im localStorage */
function saveToken(token: string): void {
	localStorage.setItem('token', token);
}

/** Hilfsfunktion: löscht den JWT (Logout) */
export function logout(): void {
	localStorage.removeItem('token');
}

/** Gibt true zurück, wenn ein Token gespeichert ist */
export function isLoggedIn(): boolean {
	return getToken() !== null;
}

/**
 * Login via OAuth2 Password Flow.
 * Sendet username + password als Formular-Daten (nicht JSON!) an POST /token.
 * Speichert den erhaltenen access_token im localStorage.
 */
export async function login(username: string, password: string) {
	const formData = new URLSearchParams();
	formData.append('username', username);
	formData.append('password', password);

	let res: Response;

	try {
		res = await fetch(`${API_BASE}/token`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
			body: formData
		});
	} catch (error) {
		throw new Error("Netzwerkfehler: Der Server ist nicht erreichbar.");
	}

	if (!res.ok) {
		if (res.status === 401 || res.status === 422) {
			throw new Error("Benutzername oder Passwort falsch.");
		}  else if (res.status >= 500) {
			throw new Error(`Serverfehler (${res.status}): Bitte versuche es später erneut.`);
		} else {
			throw new Error(`Ein unerwarteter Fehler ist aufgetreten (Fehlercode: ${res.status}).`);
		}
	}

	const data = await res.json();
	saveToken(data.access_token);
}

/**
 * Führt einen authentifizierten GET-Request aus.
 * Hängt den Bearer-Token aus dem localStorage als Authorization-Header an.
 */
export async function fetchProtected<T>(path: string): Promise<T> {
	const token = getToken();

	if (!token) {
		logout();
		throw new Error('Nicht authentifiziert. Kein Token gefunden.');
	}

	const res = await fetch(`${API_BASE}${path}`, {
		method: 'GET',
		headers: {
			'Authorization': `Bearer ${token}`,
			'Content-Type': 'application/json'
		}
	});

	if (res.status === 401) {
		logout();
		throw new Error('Sitzung abgelaufen oder ungültig. Bitte logge dich erneut ein.');
	}

	if (!res.ok) {
		throw new Error(`HTTP Fehler: ${res.status}`);
	}

	return (await res.json()) as T;
}

/**
 * Führt einen nicht authentifizierten GET-Request aus.
 */
export async function fetchPublic<T>(path: string): Promise<T> {
	const res = await fetch(`${API_BASE}${path}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
	});

	if (!res.ok) {
		throw new Error(`HTTP Fehler: ${res.status}`);
	}

	return (await res.json()) as T;
}

export async function register(username: string, email: string, password: string): Promise<void> {
	let res: Response;

	try {
		res = await fetch(`${API_BASE}/auth/register`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ username, email, password })
		});
	} catch (error) {
		throw new Error("Netzwerkfehler: Der Server ist nicht erreichbar.");
	}

	if (!res.ok) {
		if (res.status === 400 || res.status === 409) {
			const errorData = await res.json().catch(() => null);

			// Reagiert direkt auf die "User existiert bereits" Meldung aus deiner main.py
			if (errorData?.detail?.includes("existiert bereits")) {
				throw new Error("Dieser Benutzername oder diese E-Mail ist leider schon vergeben.");
			}

			throw new Error(errorData?.detail || "Registrierung fehlgeschlagen. Überprüfe deine Eingaben.");
		} else if (res.status >= 500) {
			throw new Error(`Serverfehler (${res.status}): Die Registrierung ist derzeit nicht möglich.`);
		} else {
			throw new Error(`Ein unerwarteter Fehler ist aufgetreten (Code: ${res.status}).`);
		}
	}
}
