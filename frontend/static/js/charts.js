async function loadCharts() {
    await Promise.all([
        loadEfficiencyChart(),
        loadPowerChart(),
        loadStatusChart(),
        loadCO2Chart()
    ]);
}

async function loadEfficiencyChart() {
    try {
        const response = await fetchWithAuth(`${API_BASE}/analytics/kpis/history?hours=24`);
        if (response && response.ok) {
            const data = await response.json();
            renderEfficiencyChart(data);
        }
    } catch (error) {
        console.error('Error loading efficiency chart:', error);
    }
}

function renderEfficiencyChart(data) {
    const ctx = document.getElementById('efficiencyChart');
    if (!ctx) return;
    
    if (window.efficiencyChartInstance) {
        window.efficiencyChartInstance.destroy();
    }
    
    const labels = data.map(d => {
        const date = new Date(d.timestamp);
        return date.getHours() + ':00';
    });
    
    window.efficiencyChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Overall Efficiency (%)',
                data: data.map(d => d.overall_efficiency),
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 70,
                    max: 100
                }
            }
        }
    });
}

async function loadPowerChart() {
    try {
        const response = await fetchWithAuth(`${API_BASE}/analytics/kpis/history?hours=24`);
        if (response && response.ok) {
            const data = await response.json();
            renderPowerChart(data);
        }
    } catch (error) {
        console.error('Error loading power chart:', error);
    }
}

function renderPowerChart(data) {
    const ctx = document.getElementById('powerChart');
    if (!ctx) return;
    
    if (window.powerChartInstance) {
        window.powerChartInstance.destroy();
    }
    
    const labels = data.map(d => {
        const date = new Date(d.timestamp);
        return date.getHours() + ':00';
    });
    
    window.powerChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Power Consumption (kW)',
                data: data.map(d => d.total_power_consumption),
                backgroundColor: 'rgba(241, 196, 15, 0.6)',
                borderColor: '#f39c12',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 800
                }
            }
        }
    });
}

async function loadStatusChart() {
    try {
        const response = await fetchWithAuth(`${API_BASE}/machines/`);
        if (response && response.ok) {
            const machines = await response.json();
            renderStatusChart(machines);
        }
    } catch (error) {
        console.error('Error loading status chart:', error);
    }
}

function renderStatusChart(machines) {
    const ctx = document.getElementById('statusChart');
    if (!ctx) return;
    
    if (window.statusChartInstance) {
        window.statusChartInstance.destroy();
    }
    
    const statusCounts = {};
    machines.forEach(machine => {
        statusCounts[machine.status] = (statusCounts[machine.status] || 0) + 1;
    });
    
    window.statusChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(statusCounts).map(s => s.charAt(0).toUpperCase() + s.slice(1)),
            datasets: [{
                data: Object.values(statusCounts),
                backgroundColor: [
                    'rgba(46, 204, 113, 0.8)',
                    'rgba(241, 196, 15, 0.8)',
                    'rgba(52, 152, 219, 0.8)',
                    'rgba(231, 76, 60, 0.8)'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom'
                }
            }
        }
    });
}

async function loadCO2Chart() {
    try {
        const response = await fetchWithAuth(`${API_BASE}/analytics/energy/history?hours=24`);
        if (response && response.ok) {
            const data = await response.json();
            renderCO2Chart(data);
        }
    } catch (error) {
        console.error('Error loading CO2 chart:', error);
    }
}

function renderCO2Chart(data) {
    const ctx = document.getElementById('co2Chart');
    if (!ctx) return;
    
    if (window.co2ChartInstance) {
        window.co2ChartInstance.destroy();
    }
    
    const labels = data.map(d => {
        const date = new Date(d.timestamp);
        return date.getHours() + ':00';
    });
    
    const baselineEmissions = data.length > 0 ? data[0].estimated_co2_kg / (1 - 0.15) : 500;
    
    window.co2ChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Baseline CO2 (kg)',
                data: Array(data.length).fill(baselineEmissions),
                borderColor: '#e74c3c',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                borderDash: [5, 5],
                tension: 0,
                fill: false
            }, {
                label: 'Optimized CO2 (kg)',
                data: data.map(d => d.estimated_co2_kg),
                borderColor: '#2ecc71',
                backgroundColor: 'rgba(46, 204, 113, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}