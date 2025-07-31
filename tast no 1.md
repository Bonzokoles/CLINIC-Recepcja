Cel ProjektuStworzenie prostej, w pełni funkcjonalnej aplikacji internetowej typu "System Rejestracji Przychodni" (Clinic App). Aplikacja ma składać się z backendu, frontendu i bazy danych, a całość ma być łatwa do uruchomienia za pomocą Dockera.Stos TechnologicznyBackend: Python z frameworkiem FastAPIFrontend: JavaScript z biblioteką ReactBaza Danych: PostgreSQLUruchomienie: Docker i Docker ComposeStruktura KatalogówStwórz następującą strukturę folderów i plików:/CLINIC-Recepcja
|-- .gitignore
|-- docker-compose.yml
|-- backend/
|   |-- Dockerfile
|   |-- requirements.txt
|   |-- main.py
|-- frontend/
|   |-- Dockerfile
|   |-- package.json
|   |-- src/
|   |   |-- App.js
|   |   |-- App.css
|   |   |-- index.js
Zawartość Plików1. Plik: /docker-compose.ymlTen plik zarządza całą aplikacją.version: '3.8'

services:
  db:
    image: postgres:13
    container_name: clinic_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=clinic
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    container_name: clinic_backend
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://user:password@db/clinic

  frontend:
    build: ./frontend
    container_name: clinic_frontend
    volumes:
      - ./frontend/src:/app/src
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
2. Plik: /backend/DockerfileInstrukcje budowania obrazu dla backendu.FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
3. Plik: /backend/requirements.txtLista bibliotek Pythona potrzebnych dla backendu.fastapi
uvicorn[standard]
psycopg2-binary
4. Plik: /backend/main.pyGłówna logika aplikacji backendowej.from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import time
import os

# Utworzenie instancji FastAPI
app = FastAPI()

# Konfiguracja CORS, aby frontend mógł komunikować się z backendem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Funkcja do nawiązywania połączenia z bazą danych
def get_db_connection():
    """Nawiązuje połączenie z bazą danych PostgreSQL."""
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(os.environ["DATABASE_URL"])
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            print("Błąd połączenia z bazą danych, próba ponowna za 5 sekund...")
            time.sleep(5)
    raise Exception("Nie można połączyć się z bazą danych.")

# Endpoint API do pobierania listy wizyt
@app.get("/api/appointments")
def get_appointments():
    """Pobiera listę wizyt z bazy danych."""
    # Na razie zwracamy przykładowe dane, aby uprościć start
    # W przyszłości dodamy tutaj logikę pobierania danych z bazy
    try:
        # Ten kod jest przygotowany na przyszłość, na razie nie będzie używany
        # conn = get_db_connection()
        # cur = conn.cursor()
        # cur.execute("SELECT * FROM appointments;")
        # appointments = cur.fetchall()
        # cur.close()
        # conn.close()
        
        # Przykładowe dane
        mock_appointments = [
            {"id": 1, "patient": "Jan Kowalski", "doctor": "Dr. Anna Nowak", "date": "2025-08-10 10:00", "status": "Zaplanowana"},
            {"id": 2, "patient": "Maria Wiśniewska", "doctor": "Dr. Piotr Zieliński", "date": "2025-08-10 11:30", "status": "Potwierdzona"},
            {"id": 3, "patient": "Krzysztof Wójcik", "doctor": "Dr. Anna Nowak", "date": "2025-08-11 09:00", "status": "Zaplanowana"}
        ]
        return mock_appointments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint do sprawdzania statusu API
@app.get("/")
def read_root():
    return {"status": "API Działa Poprawnie"}
5. Plik: /frontend/DockerfileInstrukcje budowania obrazu dla frontendu.FROM node:16

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

CMD ["npm", "start"]
6. Plik: /frontend/package.jsonKonfiguracja i zależności projektu React.{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^17.0.2",
    "react-dom": "^17.0.2",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
7. Plik: /frontend/src/App.jsGłówny komponent aplikacji React.import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Adres URL naszego backendu w środowisku Docker
    const apiUrl = 'http://localhost:8000/api/appointments';

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Błąd sieci lub serwera');
        }
        return response.json();
      })
      .then(data => {
        setAppointments(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error.toString());
        setLoading(false);
        console.error("Błąd podczas pobierania danych:", error);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>System Rejestracji Przychodni</h1>
      </header>
      <main>
        <h2>Zaplanowane wizyty</h2>
        {loading && <p>Ładowanie danych...</p>}
        {error && <p className="error-message">Nie można załadować danych: {error}</p>}
        {!loading && !error && (
          <table>
            <thead>
              <tr>
                <th>Pacjent</th>
                <th>Lekarz</th>
                <th>Data wizyty</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map((apt) => (
                <tr key={apt.id}>
                  <td>{apt.patient}</td>
                  <td>{apt.doctor}</td>
                  <td>{apt.date}</td>
                  <td>{apt.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </main>
    </div>
  );
}

export default App;
8. Plik: /frontend/src/App.cssStyle dla aplikacji React.body {
  background-color: #f4f7f6;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  margin: 0;
  color: #333;
}

.App {
  text-align: center;
}

.App-header {
  background-color: #e3f2fd;
  padding: 20px;
  color: #1e3a8a;
  border-bottom: 2px solid #bbdefb;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.App-header h1 {
  margin: 0;
  font-size: 2rem;
}

main {
  padding: 20px;
}

main h2 {
  color: #1e3a8a;
}

table {
  width: 90%;
  max-width: 1000px;
  margin: 20px auto;
  border-collapse: collapse;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  padding: 15px;
  border-bottom: 1px solid #ddd;
  text-align: left;
}

thead {
  background-color: #bbdefb;
  color: #1e3a8a;
  font-weight: bold;
}

tbody tr:nth-child(even) {
  background-color: #f8f9fa;
}

tbody tr:hover {
  background-color: #e3f2fd;
}

.error-message {
  color: #d32f2f;
  background-color: #ffcdd2;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #d32f2f;
}
9. Plik: /frontend/src/index.jsGłówny plik wejściowy dla aplikacji React.import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
10. Plik: /.gitignorePlik określający, które pliki i foldery mają być ignorowane przez Git.# Zależności
/node_modules
/backend/__pycache__

# Pliki środowiskowe
.env
.env.local

# Pliki produkcyjne
/build
