const API_BASE = 'http://localhost:8000/api/v1';

function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token && !window.location.pathname.includes('index.html') && window.location.pathname !== '/') {
        window.location.href = '/index.html';
    }
}

function displayUserInfo() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
        const userInfoDiv = document.getElementById('userInfo');
        if (userInfoDiv) {
            userInfoDiv.innerHTML = `
                <div>Logged in as: <strong>${user.username}</strong></div>
                <div>Role: <span class="role-badge">${user.role}</span></div>
            `;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = '/index.html';
        });
    }
});

async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('access_token');
    const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    const response = await fetch(url, { ...options, headers });
    
    if (response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/index.html';
        return null;
    }
    
    return response;
}

async function initializeDashboard() {
    await Promise.all([
        loadKPIs(),
        loadCharts(),
        loadAlerts(),
        loadMachinesOverview()
    ]);
}

async function loadKPIs() {
    try {
        const response = await fetchWithAuth(`${API_BASE}/analytics/kpis/current`);
        if (response && response.ok) {
            const data = await response.json();
            updateKPICards(data);
        }
    } catch (error) {
        console.error('Error loading KPIs:', error);
    }
}

function updateKPICards(data) {
    document.getElementById('efficiency').textContent = data.overall_efficiency.toFixed(1) + '%';
    document.getElementById('health').textContent = data.average_health.toFixed(1) + '%';
    document.getElementById('power').textContent = data.total_power_consumption.toFixed(1) + ' kW';
    document.getElementById('failureRisk').textContent = (data.failure_risk * 100).toFixed(1) + '%';
    
    document.getElementById('efficiencyChange').textContent = '+2.3%';
    document.getElementById('healthChange').textContent = '+1.5%';
    document.getElementById('powerChange').textContent = '-3.2%';
    document.getElementById('riskChange').textContent = '-5.1%';
    
    document.getElementById('lastUpdate').textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
}

async function loadAlerts() {
    try {
        const response = await fetchWithAuth(`${API_BASE}/alerts/?limit=5`);
        if (response && response.ok) {
            const alerts = await response.json();
            displayAlerts(alerts);
        }
    } catch (error) {
        console.error('Error loading alerts:', error);
    }
}

function displayAlerts(alerts) {
    const alertsList = document.getElementById('alertsList');
    if (!alertsList) return;
    
    alertsList.innerHTML = '';
    
    if (alerts.length === 0) {
        alertsList.innerHTML = '<p>No recent alerts</p>';
        return;
    }
    
    alerts.forEach(alert => {
        const alertItem = document.createElement('div');
        alertItem.className = `alert-item ${alert.severity}`;
        alertItem.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <strong>${alert.machine_id}</strong> - ${alert.message}
                    <div style="font-size: 12px; color: #7f8c8d; margin-top: 5px;">
                        ${new Date(alert.timestamp).toLocaleString()}
                    </div>
                </div>
                <span class="status-badge ${alert.severity}">${alert.severity}</span>
            </div>
        `;
        alertsList.appendChild(alertItem);
    });
}

async function loadMachinesOverview() {
    try {
        const response = await fetchWithAuth(`${API_BASE}/machines/`);
        if (response && response.ok) {
            const machines = await response.json();
            displayMachinesOverview(machines.slice(0, 12));
        }
    } catch (error) {
        console.error('Error loading machines:', error);
    }
}

function displayMachinesOverview(machines) {
    const machinesList = document.getElementById('machinesList');
    if (!machinesList) return;
    
    machinesList.innerHTML = '';
    
    machines.forEach(machine => {
        const card = document.createElement('div');
        card.className = 'machine-card';
        card.onclick = () => window.location.href = `/machines.html?id=${machine.machine_id}`;
        
        const healthClass = machine.health_score >= 80 ? 'good' : machine.health_score >= 60 ? 'warning' : 'critical';
        
        card.innerHTML = `
            <h4>${machine.machine_id}</h4>
            <span class="status ${machine.status}">${machine.status}</span>
            <div class="health ${healthClass}">${machine.health_score.toFixed(0)}%</div>
            <div style="font-size: 12px; color: #7f8c8d;">Health Score</div>
        `;
        
        machinesList.appendChild(card);
    });
}

async function refreshData() {
    await initializeDashboard();
}

function formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleString();
}

function getStatusColor(status) {
    const colors = {
        'operational': '#2ecc71',
        'maintenance': '#f39c12',
        'standby': '#3498db',
        'offline': '#e74c3c'
    };
    return colors[status] || '#95a5a6';
}

function getSeverityColor(severity) {
    const colors = {
        'critical': '#e74c3c',
        'high': '#f39c12',
        'medium': '#3498db',
        'low': '#95a5a6'
    };
    return colors[severity] || '#95a5a6';
}