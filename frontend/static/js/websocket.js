class FactoryBrainWebSocket {
    constructor() {
        this.ws = null;
        this.reconnectInterval = 5000;
        this.handlers = {};
    }
    
    connect() {
        const token = localStorage.getItem('access_token');
        if (!token) return;
        
        this.ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.onConnectionChange(true);
        };
        
        this.ws.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                this.handleMessage(message);
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.onConnectionChange(false);
            setTimeout(() => this.connect(), this.reconnectInterval);
        };
    }
    
    handleMessage(message) {
        const { type, data } = message;
        
        if (this.handlers[type]) {
            this.handlers[type].forEach(handler => handler(data));
        }
    }
    
    on(type, handler) {
        if (!this.handlers[type]) {
            this.handlers[type] = [];
        }
        this.handlers[type].push(handler);
    }
    
    send(type, data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ type, data }));
        }
    }
    
    onConnectionChange(connected) {
        const statusIndicator = document.getElementById('wsStatus');
        if (statusIndicator) {
            statusIndicator.className = connected ? 'connected' : 'disconnected';
            statusIndicator.textContent = connected ? 'Live' : 'Reconnecting...';
        }
    }
    
    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

const wsClient = new FactoryBrainWebSocket();

if (window.location.pathname.includes('dashboard.html')) {
    wsClient.connect();
    
    wsClient.on('sensor_update', (data) => {
        console.log('Sensor update:', data);
        updateMachineSensor(data);
    });
    
    wsClient.on('alert', (data) => {
        console.log('New alert:', data);
        showAlertNotification(data);
    });
    
    wsClient.on('kpi_update', (data) => {
        console.log('KPI update:', data);
        updateKPICards(data);
    });
}

function updateMachineSensor(data) {
    const machineCard = document.querySelector(`[data-machine-id="${data.machine_id}"]`);
    if (machineCard) {
        const healthElement = machineCard.querySelector('.health');
        if (healthElement) {
            healthElement.textContent = data.health_score.toFixed(0) + '%';
        }
    }
}

function showAlertNotification(alert) {
    const notification = document.createElement('div');
    notification.className = `notification ${alert.severity}`;
    notification.innerHTML = `
        <strong>${alert.machine_id}</strong>: ${alert.message}
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}