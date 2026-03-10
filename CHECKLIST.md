# ✅ Checklist di Verifica - Registro Elettronico

Usa questa checklist per verificare che tutto sia stato configurato correttamente.

## 🔐 Keycloak Configuration

- [ ] Docker Compose avviato: `docker-compose up -d` in cartella keycloak/
- [ ] Keycloak admin console accessibile: http://localhost:8080
- [ ] Login admin console con admin/admin
- [ ] Realm "Registro" creato
- [ ] Client "frontend" creato con:
  - [ ] Access Type: public
  - [ ] Valid Redirect URIs: http://localhost:4200/*
  - [ ] Web Origins: *
- [ ] Ruolo "docente" creato nel realm
- [ ] Ruolo "studente" creato nel realm
- [ ] Utente "docente1" creato con role "docente"
- [ ] Utente "mario.rossi" creato con role "studente"
- [ ] Entrambi gli utenti hanno password configurata

## 🐍 Backend (Flask) Configuration

- [ ] Python environment creato: `pip install -r requirements.txt`
- [ ] File `~/app.py` contiene decorators `@token_required` e `@role_required`
- [ ] File `db_wrapper.py` ha error handling e auto-reconnect
- [ ] Endpoint `/health` disponibile
- [ ] Endpoint `/votes` (POST) protetto con role docente
- [ ] Endpoint `/votes` (GET) protetto con role docente
- [ ] Endpoint `/my-votes` (GET) protetto con role studente
- [ ] Server Flask avviato: `python app.py`
- [ ] Backend raggiungibile: http://localhost:5000

## 🎨 Frontend (Angular) Configuration

- [ ] Node modules installati: `npm install`
- [ ] File `environment.ts` contiene:
  - [ ] keycloak.url corretto
  - [ ] keycloak.realm: "Registro"
  - [ ] keycloak.clientId: "frontend"
  - [ ] apiUrl: http://localhost:5000 o URL produzione
- [ ] File `http.interceptor.ts` esiste e aggiunge Bearer token
- [ ] File `app.config.ts` registra l'interceptor
- [ ] Role guard implementato correttamente
- [ ] Route /docente protetta con roleGuard
- [ ] Route /studente protetta con roleGuard
- [ ] Route /accesso-negato accessibile
- [ ] Componente docente importa FormsModule
- [ ] Componente studente ha calculateAverage()
- [ ] Dev server avviato: `npm start`
- [ ] Frontend raggiungibile: http://localhost:4200

## 💾 Database Configuration

- [ ] MySQL database online (Aiven) è accessibile
- [ ] Tabella `votes` creata con:
  ```sql
  CREATE TABLE IF NOT EXISTS votes (
      id INT AUTO_INCREMENT PRIMARY KEY,
      student_name VARCHAR(255) NOT NULL,
      subject VARCHAR(255) NOT NULL,
      vote INT NOT NULL
  );
  ```
- [ ] Credenziali DB in `db_wrapper.py` sono corrette

## 🧪 Functional Testing

### Test Login & Routing
- [ ] Accedi a http://localhost:4200
- [ ] Clicca "Login"
- [ ] Accedi come "docente1" / "password123"
- [ ] Sei reindirizzato a /docente
- [ ] Logout e accedi come "mario.rossi" / "password123"
- [ ] Sei reindirizzato a /studente

### Test Docente Features
- [ ] Visualizzi il form per inserire voti
- [ ] Inserisci un voto con successo
- [ ] Visualizzi la tabella con tutti i voti
- [ ] Puoi visualizzare i voti di tutti gli studenti

### Test Studente Features
- [ ] Visualizzi solo i tuoi voti
- [ ] Vedi la media voti calcolata
- [ ] Non puoi accedere a /docente (redirect a /accesso-negato)

### Test Access Control
- [ ] Docente non può accedere a /studente
- [ ] Docente vede pagina "Accesso Negato" con emoji
- [ ] Studente non può accedere a /docente
- [ ] Studente vede pagina "Accesso Negato"

### Test Error Handling
- [ ] Prova a chiamare un endpoint senza token (dovrebbe ritornare 401)
- [ ] Prova a inserire voto senza compilare campi (validation message)
- [ ] Prova a inserire voto non valido (0-10) (error message)

## 📝 Documentation

- [ ] README.md aggiornato
- [ ] SETUP_GUIDE.md creato con istruzioni complete
- [ ] CHECKLIST.md (this file) creato

## 🚀 Deployment Ready

- [ ] Tutto il codice è committed in Git
- [ ] Frontend build test: `npm build` (no errors)
- [ ] Backend è robusto con error handling
- [ ] Database backup/salvataggio configurato

## 🆘 Common Issues Fixed

- [ ] HTTP Interceptor aggiunge token Bearer ✓
- [ ] Role guard usa metodo `isLoggedIn()` ✓
- [ ] Decorators Flask hanno `@wraps` ✓
- [ ] Environment URL configurato ✓
- [ ] CORS abilitato ✓

---

**Se tutti gli item sono checkati, l'applicazione è pronta per l'uso! 🎉**
