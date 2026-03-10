#!/usr/bin/env python3
import requests
import json
import time
import sys

# Configurazione
KEYCLOAK_URL = "https://expert-disco-v6x6wrjvpp992x54r-8080.app.github.dev"
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

def create_realm(token):
    """Crea il realm Registro se non esiste"""
    url = f"{KEYCLOAK_URL}/admin/realms"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "realm": REALM,
        "enabled": True,
        "displayName": "Registro Elettronico"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            print(f"✅ Realm '{REALM}' creato")
            return True
        elif response.status_code == 409:
            print(f"⚠️  Realm '{REALM}' già esiste")
            return True
        else:
            print(f"❌ Errore nella creazione realm: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

def create_role(token, role_name):
    """Crea un ruolo nel realm"""
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/roles"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": role_name,
        "description": f"Ruolo {role_name}"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [201, 200]:
            print(f"✅ Ruolo '{role_name}' creato")
            return True
        elif response.status_code == 409:
            print(f"⚠️  Ruolo '{role_name}' già esiste")
            return True
        else:
            print(f"❌ Errore nella creazione ruolo '{role_name}': {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

def get_user_id(token, username):
    """Ottieni l'ID di un utente"""
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users?username={username}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            users = response.json()
            if users:
                return users[0]['id']
        return None
    except Exception as e:
        print(f"❌ Errore nel recupero ID utente: {e}")
        return None

def get_role_id(token, role_name):
    """Ottieni l'ID di un ruolo del realm"""
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/roles/{role_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['id']
        return None
    except Exception as e:
        return None

def assign_role_to_user(token, user_id, role_id, role_name):
    """Assegna un ruolo a un utente"""
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users/{user_id}/role-mappings/realm"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = [{
        "id": role_id,
        "name": role_name
    }]
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 204:
            print(f"  ✅ Ruolo '{role_name}' assegnato a utente")
            return True
        elif response.status_code == 409:
            print(f"  ⚠️  Ruolo già assegnato")
            return True
        else:
            print(f"  ❌ Errore nell'assegnazione: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Errore: {e}")
        return False

def main():
    print("🔐 Setup completo di Keycloak\n")
    
    # Ottieni il token
    print("🔑 Autenticazione...")
    token = get_admin_token()
    if not token:
        sys.exit(1)
    print("✅ Autenticazione riuscita\n")
    
    # Crea il realm
    print("🏰 Creazione realm...\n")
    if not create_realm(token):
        print("❌ Impossibile creare il realm. Uscita.")
        sys.exit(1)
    
    # Crea i ruoli
    print("📋 Creazione ruoli...\n")
    roles = ["docente", "studente"]
    for role in roles:
        create_role(token, role)
    
    print("\n👥 Assegnazione ruoli agli utenti...\n")
    
    users_roles = [
        ("docente1", "docente"),
        ("mario.rossi", "studente")
    ]
    
    for username, role in users_roles:
        print(f"Utente '{username}':")
        user_id = get_user_id(token, username)
        if user_id:
            role_id = get_role_id(token, role)
            if role_id:
                assign_role_to_user(token, user_id, role_id, role)
            else:
                print(f"  ❌ Ruolo '{role}' non trovato")
        else:
            print(f"  ❌ Utente '{username}' non trovato")
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETATO!")
    print("="*60)
    print("\n📝 Credenziali di test:")
    print("  👨‍🏫 Docente: docente1 / password123")
    print("  👨‍🎓 Studente: mario.rossi / password123")
    print("\n🌐 Link dell'app:")
    print("  🔗 https://expert-disco-v6x6wrjvpp992x54r-4200.app.github.dev")
    print("\nAdesso puoi fare il login!")

if __name__ == "__main__":
    main()
