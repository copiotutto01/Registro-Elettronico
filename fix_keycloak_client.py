#!/usr/bin/env python3
import requests
import json
import time
import sys

# Configurazione
KEYCLOAK_URL = "http://localhost:8080"
REALM = "Registro"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

def get_admin_token():
    """Ottieni il token admin da Keycloak"""
    token_url = f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
    payload = {
        "client_id": "admin-cli",
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD,
        "grant_type": "password"
    }

    try:
        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            print(f"❌ Errore nell'autenticazione: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")
        return None

def get_client_id(token, client_name):
    """Ottieni l'ID del client"""
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/clients"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            clients = response.json()
            for client in clients:
                if client['clientId'] == client_name:
                    return client['id']
        return None
    except Exception as e:
        print(f"❌ Errore nel recupero client: {e}")
        return None

def update_client_to_confidential(token, client_id):
    """Aggiorna il client a confidential e genera client secret"""
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/clients/{client_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Prima aggiorna il client a confidential
    payload = {
        "publicClient": False,
        "directAccessGrantsEnabled": True,
        "serviceAccountsEnabled": True,
        "implicitFlowEnabled": False,
        "standardFlowEnabled": True,
        "authorizationServicesEnabled": False
    }

    try:
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code not in [200, 204]:
            print(f"❌ Errore nell'aggiornamento client: {response.status_code}")
            print(response.text)
            return None

        print("✅ Client aggiornato a confidential")

        # Ora genera il client secret
        secret_url = f"{url}/client-secret"
        response = requests.post(secret_url, headers=headers)
        if response.status_code == 200:
            secret_data = response.json()
            client_secret = secret_data.get('value')
            print("✅ Client secret generato")
            return client_secret
        else:
            print(f"❌ Errore nella generazione secret: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Errore: {e}")
        return None

def main():
    print("🔧 Configurazione Client Keycloak per Backend\n")

    # Ottieni il token
    print("🔑 Autenticazione...")
    token = get_admin_token()
    if not token:
        sys.exit(1)
    print("✅ Autenticazione riuscita\n")

    # Trova il client frontend
    print("🔍 Ricerca client 'frontend'...")
    client_id = get_client_id(token, "frontend")
    if not client_id:
        print("❌ Client 'frontend' non trovato")
        sys.exit(1)
    print(f"✅ Client trovato: {client_id}\n")

    # Aggiorna il client
    print("🔄 Aggiornamento client a confidential...")
    client_secret = update_client_to_confidential(token, client_id)
    if not client_secret:
        sys.exit(1)

    print("\n" + "="*60)
    print("✅ CONFIGURAZIONE COMPLETATA!")
    print("="*60)
    print("\n📝 Credenziali Client:")
    print(f"  Client ID: frontend")
    print(f"  Client Secret: {client_secret}")
    print("\n🔧 Aggiorna il backend con queste credenziali!")

if __name__ == "__main__":
    main()
