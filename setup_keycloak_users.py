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
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")
        return None

def create_user(token, username, firstname, lastname, email, password):
    """Crea un utente in Keycloak"""
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM}/users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "username": username,
        "firstName": firstname,
        "lastName": lastname,
        "email": email,
        "enabled": True,
        "credentials": [{
            "type": "password",
            "value": password,
            "temporary": False
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [201, 200]:
            print(f"✅ Utente '{username}' creato con successo")
            return True
        elif response.status_code == 409:
            print(f"⚠️  Utente '{username}' già esiste")
            return True
        else:
            print(f"❌ Errore nella creazione di '{username}': {response.status_code}")
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
        print(f"❌ Errore nel recupero ID ruolo: {e}")
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
            print(f"✅ Ruolo '{role_name}' assegnato con successo")
            return True
        else:
            print(f"❌ Errore nell'assegnazione ruolo: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

def main():
    print("🔐 Creazione utenti in Keycloak...\n")
    
    # Attendere che Keycloak sia pronto
    print("Attendendo che Keycloak sia pronto...")
    for i in range(10):
        try:
            requests.get(f"{KEYCLOAK_URL}/health", timeout=2)
            print("✅ Keycloak è online\n")
            break
        except:
            if i < 9:
                time.sleep(2)
            else:
                print("❌ Keycloak non è raggiungibile")
                sys.exit(1)
    
    # Ottieni il token
    print("🔑 Autenticazione come admin...")
    token = get_admin_token()
    if not token:
        sys.exit(1)
    print("✅ Autenticazione riuscita\n")
    
    # Crea gli utenti
    users_to_create = [
        ("docente1", "Mario", "Bianchi", "docente1@scuola.it", "password123", "docente"),
        ("mario.rossi", "Mario", "Rossi", "mario.rossi@scuola.it", "password123", "studente")
    ]
    
    print("👥 Creazione utenti...\n")
    for username, firstname, lastname, email, password, role in users_to_create:
        # Crea l'utente
        if create_user(token, username, firstname, lastname, email, password):
            # Ottieni l'ID dell'utente
            user_id = get_user_id(token, username)
            if user_id:
                # Ottieni l'ID del ruolo
                role_id = get_role_id(token, role)
                if role_id:
                    # Assegna il ruolo
                    assign_role_to_user(token, user_id, role_id, role)
                else:
                    print(f"⚠️  Ruolo '{role}' non trovato")
            else:
                print(f"⚠️  Impossibile trovare l'ID dell'utente '{username}'")
        time.sleep(0.5)
    
    print("\n" + "="*50)
    print("✅ Setup completato!")
    print("="*50)
    print("\n📝 Credenziali di test:")
    print("  Docente: docente1 / password123")
    print("  Studente: mario.rossi / password123")
    print("\n🔗 Accedi all'app: https://expert-disco-v6x6wrjvpp992x54r-4200.app.github.dev")

if __name__ == "__main__":
    main()
