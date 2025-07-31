# Dashboard Frontend for Monitoring POLACZEK Automation in Real-Time

This document provides a React component setup for creating a dashboard to monitor POLACZEK automation in real-time.

## Overview
The dashboard will display real-time data regarding the automation processes, including status updates, logs, and metrics.

## Requirements
- React (Create React App)
- Axios for API requests
- Chart.js or any other charting library for visualizations

## Installation
You can create a new React app and install the required libraries using the following commands:
```bash
npx create-react-app polaczek-dashboard
cd polaczek-dashboard
npm install axios chart.js react-chartjs-2
```

## Dashboard Component
Create a new file named `Dashboard.js` in the `src` directory with the following content:

```javascript
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';

const Dashboard = () => {
    const [data, setData] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/status'); // Update with your API endpoint
                setData(response.data);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
        const interval = setInterval(fetchData, 5000); // Fetch data every 5 seconds
        return () => clearInterval(interval);
    }, []);

    if (loading) return <div>Loading...</div>;

    const chartData = {
        labels: data.labels, // Assuming your API returns labels
        datasets: [
            {
                label: 'Automation Status',
                data: data.values, // Assuming your API returns values
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
            },
        ],
    };

    return (
        <div>
            <h1>POLACZEK Automation Dashboard</h1>
            <Bar data={chartData} options={{ responsive: true }} />
            <div>
                <h2>Logs</h2>
                <pre>{JSON.stringify(data.logs, null, 2)}</pre> {/* Assuming logs are part of the response */}
            </div>
        </div>
    );
};

export default Dashboard;
```

## App Component
Update the `App.js` file to include the `Dashboard` component:

```javascript
import React from 'react';
import Dashboard from './Dashboard';

const App = () => {
    return (
        <div className="App">
            <Dashboard />
        </div>
    );
};

export default App;
```

## Running the Dashboard
1. Start your backend server that provides the API for monitoring POLACZEK automation.
2. Run the React app:
   ```bash
   npm start
   ```
3. Open your web browser and navigate to `http://localhost:3000` to view the dashboard.

## Conclusion
This React component setup provides a real-time monitoring dashboard for POLACZEK automation, allowing users to visualize status updates and logs effectively.