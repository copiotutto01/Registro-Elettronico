# 📚 Registro Elettronico

Applicazione completa per la gestione di voti scolastici con autenticazione e autorizzazione tramite Keycloak.

## 📋 Funzionalità

### Ruolo Docente 👨‍🏫
- ✏️ Inserire voti per gli studenti (nome, materia, voto)
- 📊 Visualizzare tutti i voti di tutti gli studenti
- 🔐 Accesso esclusivo alla sezione docente

### Ruolo Studente 👨‍🎓
- 📚 Visualizzare solo i propri voti
- 📈 Vedere la media dei propri voti
- 🔐 Accesso esclusivo alla sezione studente

## 🏗️ Architettura

```
Registro-Elettronico/
├── frontend/registro-frontend/     # Applicazione Angular moderna
│   ├── src/app/
│   │   ├── docente/               # Componente per i docenti
│   │   ├── studente/              # Componente per gli studenti
│   │   ├── accesso-negato/        # Pagina di errore autorizzazione
│   │   ├── auth.ts                # Servizio autenticazione
│   │   ├── role-guard.ts          # Guard per proteggere le route
│   │   └── http.interceptor.ts    # Interceptor per aggiungere token JWT
│   └── environments/              # Configurazione ambiente
├── backend/                       # API Flask
│   ├── app.py                    # Server Flask con endpoint API
│   ├── db_wrapper.py             # Wrapper per query MySQL
│   └── requirements.txt          # Dipendenze Python
└── keycloak/                     # Configurazione Keycloak
    ├── docker-compose.yml        # Servizi Docker
    └── init.sql                  # Script inizializzazione DB
```

## 🔐 Autenticazione e Sicurezza

- **Keycloak**: Server OAuth 2.0 per gestire utenti e ruoli
- **JWT Tokens**: Token Bearer per autenticazione API
- **Role-Based Access Control**: Protezione route in base ai ruoli
- **HTTP Interceptor**: Token automaticamente aggiunto alle richieste
- **CORS**: Abilitato per comunicazione frontend-backend

## 🚀 Quick Start

### Prerequisiti
- Docker e Docker Compose
- Node.js 20+ e npm
- Python 3.8+

### Avvio Rapido

1. **Avvia Keycloak e Database**
```bash
cd keycloak
docker-compose up -d
```

2. **Configura Keycloak** (vedi SETUP_GUIDE.md per dettagli)

3. **Avvia Backend Flask**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

4. **Avvia Frontend Angular**
```bash
cd frontend/registro-frontend
npm install
npm start
```

Accedi a `http://localhost:4200`

## 📖 Documentazione Completa

Per la guida di configurazione completa, test di accesso e troubleshooting, consulta [SETUP_GUIDE.md](./SETUP_GUIDE.md)

## 🔑 Credenziali di Test

Dopo la configurazione di Keycloak, usa:

**Docente:**
- Username: `docente1`
- Password: `password123`

**Studente:**
- Username: `mario.rossi`
- Password: `password123`

## 🛠️ Tecnologie

- **Frontend**: Angular 21, TypeScript, RxJS
- **Backend**: Flask, PyMySQL, python-keycloak
- **Autenticazione**: Keycloak 26
- **Database**: MySQL (Aiven Cloud)
- **Container**: Docker & Docker Compose

## 📊 Endpoint API

| Metodo | Endpoint | Ruolo | Descrizione |
|--------|----------|-------|-------------|
| POST | `/votes` | Docente | Inserire un nuovo voto |
| GET | `/votes` | Docente | Visualizzare tutti i voti |
| GET | `/my-votes` | Studente | Visualizzare propri voti |
| GET | `/health` | Pubblico | Health check |

## 🐛 Troubleshooting

Consulta [SETUP_GUIDE.md](./SETUP_GUIDE.md#-troubleshooting) per i problemi comuni e le soluzioni.

---

**Sviluppato per:** Corso di Programmazione Web

✨ **Happy Learning!**
