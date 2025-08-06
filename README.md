# 🏥 RECHAB Clinic Dashboard

## 🏥 Projekt Overview

Profesjonalny dashboard do zarządzania kliniką RECHAB z integracją Google Calendar przez N8N.

## 🚀 Quick Start

### 1. Instalacja Dependencies

```bash
cd R:\CLINIC-Recepcja\CLINICreACT
npm install
```

### 2. Uruchomienie Development Server

```bash
npm start
```

Aplikacja otworzy się na `http://localhost:3060`

### 3. Google Calendar Setup

1. Przeczytaj: `GOOGLE_CALENDAR_SETUP.md`
2. Skonfiguruj Google Cloud Console
3. Pobierz `google-credentials.json`

### 4. N8N Integration Setup

1. Przeczytaj: `N8N_WORKFLOW_CONFIG.md`
2. Upewnij się że N8N działa na `http://localhost:5678`
3. Importuj workflow configuration

## 📁 Struktura Projektu

```
CLINICreACT/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Dashboard.js          # Main dashboard with stats
│   │   ├── AppointmentsList.js   # Appointments management
│   │   └── DoctorsList.js        # Doctors list & cards
│   ├── App.js                    # Main app component
│   ├── App.css                   # Styles
│   └── index.js                  # Entry point
├── package.json
└── README.md
```

## 🔗 N8N Webhooks Integration

### Webhooks Endpoints (do skonfigurowania w n8n):

- `POST /webhook/new-appointment` - Nowa wizyta
- `GET /webhook/appointments` - Lista wizyt
- `GET /webhook/doctors` - Lista lekarzy
- `GET /webhook/stats` - Statystyki dashboard

### Example N8N Workflow Setup:

1. **HTTP Request Node** → receives webhook
2. **AI Node (Ollama)** → processes appointment data
3. **Gmail Node** → sends confirmation email
4. **Calendar Node** → creates calendar event
5. **Response Node** → returns success/error

## 🎨 Features

### ✅ Zaimplementowane:

- 📊 Dashboard ze statystykami
- 📅 Lista rezerwacji z dodawaniem
- 👨‍⚕️ Lista lekarzy (table + cards view)
- 🎨 Responsive design
- 🔄 Auto-refresh co 30 sekund
- 📱 Mobile-friendly interface

### 🔄 Do zaimplementowania (N8N integration):

- Real webhooks calls zamiast mock data
- Email automation przez n8n
- SMS reminders
- Calendar sync
- AI appointment scheduling z Ollama

## 💻 VSCode Development

### Recommended Extensions:

- ES7+ React/Redux/React-Native snippets
- Prettier - Code formatter
- Auto Rename Tag
- Bracket Pair Colorizer

### Available Scripts:

```bash
npm start    # Development server
npm build    # Production build
npm test     # Run tests
```

## 🔧 Configuration

### Environment Variables (.env):

```
REACT_APP_N8N_BASE_URL=http://localhost:5678
REACT_APP_API_BASE_URL=http://localhost:5678/webhook
```

## 📞 Support

Created by JIMBO for ZENON System
Contact: System ZENON Integration

---

## 🎯 Next Steps:

1. `npm install` - Install dependencies
2. `npm start` - Start development
3. Configure n8n webhooks
4. Replace mock data with real API calls
5. Deploy to production