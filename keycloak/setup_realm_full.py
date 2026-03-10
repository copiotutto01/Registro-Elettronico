import requests

KEYCLOAK_URL = "https://expert-disco-v6x6wrjvpp992x54r-8080.app.github.dev"
ADMIN_USER = "admin"
ADMIN_PASS = "admin"
REALM_NAME = "Registro"
CLIENT_ID = "frontend"
REDIRECT_URI = "https://stunning-disco-pjx7wv4jg9gr26pvv-4200.app.github.dev/*"

USERS = [
    {"username": "docente", "password": "docente", "roles": ["docente"]},
    {"username": "studente", "password": "studente", "roles": ["studente"]},
]
ROLES = ["docente", "studente"]

# 1. Ottieni token admin
resp = requests.post(
    f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token",
    data={
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": ADMIN_USER,
        "password": ADMIN_PASS,
    },
)
resp.raise_for_status()
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 2. Crea il realm
realm_data = {"realm": REALM_NAME, "enabled": True}
resp = requests.post(f"{KEYCLOAK_URL}/admin/realms", json=realm_data, headers=headers)
if resp.status_code == 409:
    print("Realm già esistente, continuo...")
else:
    resp.raise_for_status()
    print("Realm creato!")

# 3. Crea il client
client_data = {
    "clientId": CLIENT_ID,
    "enabled": True,
    "redirectUris": [REDIRECT_URI],
    "publicClient": True,
    "protocol": "openid-connect",
    "standardFlowEnabled": True,
    "directAccessGrantsEnabled": True
}
resp = requests.post(f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/clients", json=client_data, headers=headers)
if resp.status_code == 409:
    print("Client già esistente, continuo...")
else:
    resp.raise_for_status()
    print("Client creato!")

# 4. Crea i ruoli
for role in ROLES:
    role_data = {"name": role}
    resp = requests.post(f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/roles", json=role_data, headers=headers)
    if resp.status_code == 409:
        print(f"Ruolo '{role}' già esistente, continuo...")
    else:
        resp.raise_for_status()
        print(f"Ruolo '{role}' creato!")

# 5. Crea utenti e assegna ruoli
for user in USERS:
    user_data = {
        "username": user["username"],
        "enabled": True,
        "credentials": [{"type": "password", "value": user["password"], "temporary": False}],
    }
    resp = requests.post(f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/users", json=user_data, headers=headers)
    if resp.status_code == 409:
        print(f"Utente '{user['username']}' già esistente, continuo...")
    else:
        resp.raise_for_status()
        print(f"Utente '{user['username']}' creato!")
    # Recupera l'ID utente
    resp = requests.get(f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/users", headers=headers, params={"username": user["username"]})
    resp.raise_for_status()
    user_id = resp.json()[0]["id"]
    # Recupera i ruoli
    for role in user["roles"]:
        resp_role = requests.get(f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/roles/{role}", headers=headers)
        resp_role.raise_for_status()
        role_repr = resp_role.json()
        # Assegna ruolo all'utente
        resp_assign = requests.post(
            f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/users/{user_id}/role-mappings/realm",
            json=[{"id": role_repr["id"], "name": role_repr["name"]}],
            headers=headers
        )
        if resp_assign.status_code in (204, 409):
            print(f"Ruolo '{role}' assegnato a '{user['username']}'")
        else:
            resp_assign.raise_for_status()

print("Realm, client, ruoli e utenti configurati!")
