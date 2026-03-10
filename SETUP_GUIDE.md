# 📚 Guida di Configurazione e Avvio - Registro Elettronico

## Prerequisiti
- Docker e Docker Compose per Keycloak
- Node.js 20+ e npm per il Frontend
- Python 3.8+ per il Backend
- MySQL database online (Aiven)

---

## 🔐 1. Configurare Keycloak

### Avviare Keycloak con Docker Compose
```bash
cd keycloak
docker-compose up -d
```

Keycloak sarà disponibile a: `https://expert-disco-v6x6wrjvpp992x54r-8080.app.github.dev`

### Configurare il Realm e gli Utenti

1. **Login Admin Console**
   - URL: `http://localhost:8080/admin`
   - Username: `admin`
   - Password: `admin`

2. **Creare Realm "Registro"** (se non esiste)
   - Click "Add Realm" → Name: "Registro"

3. **Creare i Ruoli nel Realm**
   - Go to "Realm Roles"
   - Add Role: `docente`
   - Add Role: `studente`

4. **Creare Client "frontend"** (se non esiste)
   - Go to "Clients"
   - Create Client: `frontend`
   - Impostazioni Client:
     - Access Type: `public`
     - Valid Redirect URIs: `http://localhost:4200/*`, `http://localhost:4200`
     - Web Origins: `*`

5. **Creare Utenti di Test**

   **Utente Docente:**
   - Username: `docente1`
   - Password: `password123`
   - Assign Role: `docente` (in Realm Roles)
   - First Name: `Mario`
   - Last Name: `Bianchi`

   **Utente Studente:**
   - Username: `mario.rossi`
   - Password: `password123`
   - Assign Role: `studente` (in Realm Roles)
   - First Name: `Mario`
   - Last Name: `Rossi`

---

## 🐍 2. Configurare e Avviare il Backend (Flask)

### Installare le Dipendenze
```bash
cd backend
pip install -r requirements.txt
```

### Verificare la Configurazione Database
Assicurarsi che le credenziali in `db_wrapper.py` siano corrette:
- Host: `mysql-3f12020f-galvani5d.j.aivencloud.com`
- User: `avnadmin`
- Password: Già configurato
- Database: `defaultdb`
- Port: `13861`

### Avviare il Server Flask
```bash
python app.py
```

Il backend sarà disponibile a: `http://localhost:5000`

### Verificare la Connessione al Database
```bash
curl http://localhost:5000/health
```

---

## 🎨 3. Configurare e Avviare il Frontend (Angular)

### Installare le Dipendenze
```bash
cd frontend/registro-frontend
npm install
```

### Verificare la Configurazione
File: `src/environments/environment.ts`
```typescript
export const environment = {
  production: false,
  keycloak: {
    url: 'https://expert-disco-v6x6wrjvpp992x54r-8080.app.github.dev',
    realm: 'Registro',
    clientId: 'frontend',
    redirectUri: window.location.origin,
  },
  apiUrl: 'https://expert-disco-v6x6wrjvpp992x54r-5000.app.github.dev',
};
```

### Avviare il Server di Sviluppo
```bash
npm start
```

L'applicazione sarà disponibile a: `http://localhost:4200`

---

## 🔄 Flusso di Utilizzo

### Login come Docente
1. Vai a `http://localhost:4200`
2. Clicca "Login"
3. Usa le credenziali:
   - Username: `docente1`
   - Password: `password123`
4. Sarai reindirizzato a `/docente`
5. Potrai:
   - ✏️ Inserire voti per gli studenti
   - 📊 Visualizzare tutti i voti

### Login come Studente
1. Vai a `http://localhost:4200`
2. Clicca "Login"
3. Usa le credenziali:
   - Username: `mario.rossi`
   - Password: `password123`
4. Sarai reindirizzato a `/studente`
5. Potrai:
   - 📚 Visualizzare solo i tuoi voti
   - 📈 Vedere la media voti

### Tentativo di Accesso non Autorizzato
- Se un docente prova ad accedere a `/studente` → Reindirizzato a `/accesso-negato`
- Se uno studente prova ad accedere a `/docente` → Reindirizzato a `/accesso-negato`

---

## 🛡️ Architettura di Sicurezza

### Frontend (Angular)
- ✅ AuthService per gestire login/logout
- ✅ HTTP Interceptor che aggiunge token Bearer a ogni richiesta
- ✅ Role Guards che proteggono le route
- ✅ Reindirizzamento automatico basato sui ruoli

### Backend (Flask)
- ✅ Token validation con Keycloak
- ✅ Role-based access control su ogni endpoint
- ✅ Decorators per token_required e role_required
- ✅ Error handling robusto

### Database
- ✅ Wrapper class per le query SQL
- ✅ Protezione dalle SQL Injection
- ✅ Gestione connessioni con auto-reconnect

---

## 🐛 Troubleshooting

### "Token is invalid"
- Verifica che Keycloak sia online e raggiungibile
- Controlla che l'URL di Keycloak nel frontend sia corretto
- Verifica che il token non sia scaduto

### "Insufficient permissions"
- Assicurati che l'utente abbia il ruolo corretto assegnato in Keycloak
- Verifica che il ruolo sia assegnato a livello di Realm Roles
- Accedi di nuovo dopo aver assegnato il ruolo

### Errore di Connessione al Database
- Verifica le credenziali MySQL
- Assicurati che la tabella `votes` esista in MySQL:
```sql
CREATE TABLE IF NOT EXISTS votes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    vote INT NOT NULL
);
```

### CORS Errors
- Assicurati che CORS sia abilitato in Flask (già fatto)
- Verifica che l'URL del backend sia corretto in environment.ts
- Controlla la console del browser per errori dettagliati

---

## 📝 Note Finali

- ✅ Autenticazione completamente funzionante con Keycloak
- ✅ Routing intelligente basato su ruoli
- ✅ Componenti docente e studente separati
- ✅ UI moderna con design responsive
- ✅ Gestione errori robusta
- ✅ Backend con role-based access control
- ✅ Database wrapper per query sicure

**Qualsiasi problema?** Controlla i log della console (frontend) e del terminale (backend) per messaggi di errore dettagliati!
