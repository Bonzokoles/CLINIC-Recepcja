from fastapi import FastAPI

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os
from datetime import datetime
import time

# --- Konfiguracja Połączenia z Bazą Danych ---
DATABASE_URL = os.environ["DATABASE_URL"]

# Pętla próbująca nawiązać połączenie z bazą danych
# Czasem backend startuje szybciej niż baza danych, więc musimy dać jej chwilę
retries = 5
while retries > 0:
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        print("Successfully connected to the database.")
        break
    except Exception as e:
        retries -= 1
        print(f"Error connecting to the database: {e}. Retrying in 5 seconds... ({retries} retries left)")
        time.sleep(5)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Model Danych (Struktura Tabeli) ---
class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient = Column(String, index=True)
    doctor = Column(String)
    date = Column(DateTime)
    status = Column(String, default="Zaplanowana")


# Tworzenie tabel w bazie danych (jeśli nie istnieją)
Base.metadata.create_all(bind=engine)

# --- Dodanie przykładowych danych, jeśli tabela jest pusta ---
def insert_sample_data():
    db = SessionLocal()
    if db.query(Appointment).count() == 0:
        sample_appointments = [
            Appointment(patient="Jan Kowalski", doctor="Dr. Nowak", date=datetime(2025, 8, 10, 10, 0), status="Zaplanowana"),
            Appointment(patient="Anna Nowak", doctor="Dr. Kowalska", date=datetime(2025, 8, 11, 12, 30), status="Potwierdzona"),
            Appointment(patient="Piotr Zielinski", doctor="Dr. Malinowski", date=datetime(2025, 8, 12, 9, 15), status="Zakończona"),
        ]
        db.add_all(sample_appointments)
        db.commit()
    db.close()

insert_sample_data()

# --- Aplikacja FastAPI ---
app = FastAPI(title="THE_DEsk_service API")

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Funkcja pomocnicza do zarządzania sesją bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints API ---
@app.get("/")
def read_root():
    return {"status": "API Działa Poprawnie i jest połączone z bazą danych"}

@app.get("/api/appointments")
def get_appointments(db: Session = Depends(get_db)):
    """Pobiera listę wszystkich wizyt z bazy danych."""
    appointments = db.query(Appointment).all()
    return appointments

# Możesz użyć tego endpointu w przyszłości do dodawania danych
# np. za pomocą narzędzia Postman lub po dodaniu formularza w frontendzie
@app.post("/api/appointments")
def create_appointment(patient: str, doctor: str, date: datetime, db: Session = Depends(get_db)):
    """Dodaje nową wizytę do bazy danych."""
    new_appointment = Appointment(patient=patient, doctor=doctor, date=date)
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment