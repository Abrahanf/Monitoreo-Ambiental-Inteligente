//<!-- frontend/static/js/dashboard.js -->
// Dashboard JS
let tempChart, humChart, co2Chart;

async function loadDashboardData() {
    try {
        const nodeId = JSON.parse(localStorage.getItem('user')).nodo_id;
        
        const response = await fetchAPI(`/measurements/dashboard/${nodeId}`);
        const data = await response.json();
        
        // Actualizar valores actuales
        if (data.latest_measurement) {
            document.getElementById('temp-value').textContent = 
                data.latest_measurement.temperatura.toFixed(1);
            document.getElementById('hum-value').textContent = 
                data.latest_measurement.humedad.toFixed(1);
            document.getElementById('co2-value').textContent = 
                data.latest_measurement.co2.toFixed(0);
        }
        
        // Actualizar contador de alertas
        document.getElementById('alerts-count').textContent = 
            data.active_alerts?.length || 0;
        
        // Actualizar gráficos
        updateCharts(data.hourly_data);
        
        // Mostrar alertas
        displayAlerts(data.active_alerts);
        
    } catch (error) {
        console.error('Error cargando dashboard:', error);
    }
}

function updateCharts(hourlyData) {
    const labels = hourlyData.map(d => new Date(d.fecha_hora).toLocaleTimeString());
    const temps = hourlyData.map(d => d.temperatura);
    const hums = hourlyData.map(d => d.humedad);
    const co2s = hourlyData.map(d => d.co2);
    
    // Temperatura
    const tempCtx = document.getElementById('tempChart').getContext('2d');
    if (tempChart) tempChart.destroy();
    tempChart = new Chart(tempCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Temperatura (°C)',
                data: temps,
                borderColor: 'rgb(239, 68, 68)',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                tension: 0.4
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
    
    // Similar para humedad y CO2...
}

function displayAlerts(alerts) {
    const alertsList = document.getElementById('alerts-list');
    
    if (!alerts || alerts.length === 0) {
        alertsList.innerHTML = '<p>No hay alertas activas</p>';
        return;
    }
    
    alertsList.innerHTML = alerts.map(alert => `
        <div class="alert-item severity-${alert.severidad.toLowerCase()}">
            <strong>${alert.tipo}</strong>
            <p>${alert.mensaje}</p>
            <span class="alert-time">${formatDate(alert.fecha_creacion)}</span>
        </div>
    `).join('');
}

// Cargar datos al inicio y actualizar cada 30 segundos
loadDashboardData();
setInterval(loadDashboardData, 30000);