# Medical Clinic System: Automation for Reception

This document outlines a complete automation system for the reception of a medical clinic, leveraging existing solutions for managing appointments, automating email communications with patients, sending SMS reminders, and integrating with doctors' calendars.

## Overview
The system will consist of the following components:
- **Appointment Management**: Handle patient bookings and manage visit schedules.
- **Email Automation**: Automate communication with patients regarding their appointments.
- **SMS Reminders**: Send reminders to patients about upcoming visits.
- **Calendar Integration**: Sync appointments with doctors' calendars.

## Components

### 1. Appointment Management
- **Database Schema**: Create tables to manage patients, appointments, and doctors.
- **API Endpoints**: Develop RESTful APIs to handle appointment bookings, cancellations, and updates.

#### SQL Tables
```sql
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    doctor_id INT REFERENCES doctors(doctor_id),
    appointment_date TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Email Automation
- **Email Service**: Use a service like SendGrid or SMTP to send appointment confirmations and reminders.
- **Email Templates**: Create templates for different types of communications (confirmation, cancellation, reminders).

#### Example Email Sending Function
```python
import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'clinic@example.com'
    msg['To'] = to_email

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('username', 'password')
        server.send_message(msg)
```

### 3. SMS Reminders
- **SMS Service**: Integrate with a service like Twilio to send SMS reminders to patients.
- **Reminder Logic**: Schedule SMS reminders to be sent 24 hours before the appointment.

#### Example SMS Sending Function
```python
from twilio.rest import Client

def send_sms(to_phone, message):
    client = Client('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN')
    client.messages.create(
        body=message,
        from_='+1234567890',
        to=to_phone
    )
```

### 4. Calendar Integration
- **Google Calendar API**: Use the Google Calendar API to sync appointments with doctors' calendars.
- **Event Creation**: Automatically create calendar events when an appointment is booked.

#### Example Calendar Event Creation
```python
from googleapiclient.discovery import build
from google.oauth2 import service_account

def create_calendar_event(doctor_email, appointment_date):
    credentials = service_account.Credentials.from_service_account_file('path/to/credentials.json')
    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': 'Appointment',
        'start': {'dateTime': appointment_date.isoformat()},
        'end': {'dateTime': (appointment_date + timedelta(hours=1)).isoformat()},
        'attendees': [{'email': doctor_email}]
    }

    service.events().insert(calendarId='primary', body=event).execute()
```

## Implementation Steps
1. **Set Up Database**: Create the necessary tables in your database.
2. **Develop APIs**: Implement the RESTful APIs for managing appointments and patients.
3. **Integrate Email and SMS Services**: Set up email and SMS services for communication.
4. **Implement Calendar Integration**: Connect to the Google Calendar API for syncing appointments.
5. **Testing**: Test the entire workflow to ensure all components work together seamlessly.

## Conclusion
This medical clinic system provides a comprehensive solution for automating reception tasks, improving patient communication, and streamlining appointment management.