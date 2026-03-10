import requests

KEYCLOAK_URL = "https://expert-disco-v6x6wrjvpp992x54r-8080.app.github.dev"
ADMIN_USER = "admin"
ADMIN_PASS = "admin"
REALM_NAME = "Registro"
CLIENT_ID = "frontend"
REDIRECT_URI = "https://stunning-disco-pjx7wv4jg9gr26pvv-4200.app.github.dev/*"

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
realm_data = {
    "realm": REALM_NAME,
    "enabled": True
}
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

print("Realm e client configurati!")
