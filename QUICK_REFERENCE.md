# 🔗 Quick Reference - URLs e Commands

## 🌐 Important URLs

### Keycloak
- Admin Console: http://localhost:8080/admin
- Realm Console: http://localhost:8080/realms/Registro
- API Token Endpoint: http://localhost:8080/realms/Registro/protocol/openid-connect/token

### Frontend
- Application: http://localhost:4200
- Docente Route: http://localhost:4200/docente
- Studente Route: http://localhost:4200/studente
- Access Denied: http://localhost:4200/accesso-negato

### Backend
- Health Check: http://localhost:5000/health
- Insert Vote: POST http://localhost:5000/votes
- Get All Votes: GET http://localhost:5000/votes
- Get My Votes: GET http://localhost:5000/my-votes

---

## 🎯 Quick Start Commands

### 1. Start Keycloak
```bash
cd keycloak
docker-compose up -d
```

### 2. Start Backend
```bash
cd backend
python app.py
```

### 3. Start Frontend
```bash
cd frontend/registro-frontend
npm start
```

### 4. Test Health
```bash
curl http://localhost:5000/health
```

---

## 👥 Test Credentials

| Ruolo | Username | Password | Redirect |
|-------|----------|----------|----------|
| Docente | docente1 | password123 | /docente |
| Studente | mario.rossi | password123 | /studente |

---

## 🔧 Database Commands

### Connect to MySQL
```bash
mysql -h mysql-3f12020f-galvani5d.j.aivencloud.com \
       -u avnadmin \
       -p'AVNS_idAGBvmY7bsHyDkUXBM' \
       -P 13861 \
       -D defaultdb
```

### Check Table Structure
```sql
DESCRIBE votes;
```

### View All Votes
```sql
SELECT * FROM votes;
```

### View Votes for Student
```sql
SELECT * FROM votes WHERE student_name = 'mario.rossi';
```

---

## 📊 API Examples

### Insert Vote (Docente only)
```bash
curl -X POST http://localhost:5000/votes \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "mario.rossi",
    "subject": "Matematica",
    "vote": 8
  }'
```

### Get All Votes (Docente only)
```bash
curl -X GET http://localhost:5000/votes \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get My Votes (Studente only)
```bash
curl -X GET http://localhost:5000/my-votes \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🐛 Debug Tips

### Frontend Console Log Token
```javascript
// In browser console
localStorage.getItem('kc_access_token')
```

### Backend Logs
- Check Flask server output for printed debug messages
- Look for "Token validation error" or database connection errors

### Check Network Requests
- Open DevTools (F12) → Network tab
- Look for Authorization header in requests

---

## 📦 File Structure Quick Reference

```
src/app/
├── auth.ts                 # AuthService
├── http.interceptor.ts     # Token interceptor
├── role-guard.ts           # Route guard
├── app.ts                  # Main component
├── app.routes.ts           # Routes configuration
├── docente/
│   ├── docente.ts          # Docente component
│   ├── docente.html        # Docente template
│   └── docente.css         # Docente styles
├── studente/
│   ├── studente.ts         # Studente component
│   ├── studente.html       # Studente template
│   └── studente.css        # Studente styles
└── accesso-negato/
    ├── accesso-negato.ts   # Error component
    ├── accesso-negato.html # Error template
    └── accesso-negato.css  # Error styles

backend/
├── app.py                  # Flask routes
├── db_wrapper.py           # Database wrapper
└── requirements.txt        # Dependencies
```

---

## 🆘 Emergency Contacts / Solutions

### Port Already in Use
```bash
# Check what's using port 4200
lsof -i :4200

# Kill process
kill -9 PID
```

### Clear Angular Cache
```bash
rm -rf node_modules
rm package-lock.json
npm install
npm start
```

### Reset Keycloak
```bash
docker-compose down -v  # Remove volumes
docker-compose up -d    # Start fresh
```

---

**Last Updated**: 2024-2026
**Project**: Registro Elettronico - Gestione Voti Scolastici
