import React, { useState, useEffect } from 'react';
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
        <h1>THE_DEsk_service</h1>
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
