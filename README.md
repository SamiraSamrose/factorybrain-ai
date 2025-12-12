# FactoryBrain AI

Autonomous Process Optimization for Smart Manufacturing Plants

## Overview

FactoryBrain AI is a comprehensive multi-agent industrial control system that monitors machinery, predicts failures, optimizes energy usage, negotiates spare-part procurement and communicates with operators using natural voice interfaces.

The project focuses on advancing robotics and automation, drawing inspiration from leaders such as Google DeepMind’s industrial AI, Amazon Robotics. It emphasizes ultra-low-latency inference for IoT and edge devices to enable real-time decision-making. Enterprise-grade AI agents are designed to deliver massive-scale optimization across complex operations. The work aligns closely with the priorities of teams at Amazon Robotics, Google Cloud, Meta Infrastructure and AWS IoT. By reducing downtime and boosting efficiency at scale, the solution saves millions and industries strongly value infrastructure that delivers this level of performance.

## Links

- **Live Site Demo**: https://samirasamrose.github.io/factorybrain-ai/
- **Source Code**: https://github.com/SamiraSamrose/factorybrain-ai
- **Video Demo**: https://youtu.be/IZHyU37i_q4

## Key Features

### AI Agent System
- **Plant Optimization Agent**: Monitors KPIs, directs sub-agents, optimizes workloads
- **Anomaly Detection Agent**: Real-time fault detection using Cerebras ultra-low latency inference
- **Procurement Agent**: Autonomous spare parts ordering with supplier negotiation
- **Energy Optimizer Agent**: CO2 reduction through intelligent energy management

### Voice Interface
- ElevenLabs voice assistant for operator alerts
- Natural language repair instructions
- Voice logging of operator commands

### Predictive Maintenance
- Machine failure prediction with remaining useful life estimation
- Vibration and acoustic analysis
- Multi-sensor anomaly detection

### Energy Optimization
- 20% CO2 emissions reduction target
- Off-peak operation scheduling
- Real-time power consumption monitoring

### List of Core Features 
- **Real-Time Machine Monitoring**: Tracks temperature, vibration, pressure, power consumption from 20+ machines with 30-second data refresh, displays current readings and 24-hour history charts on dashboard.
- **Anomaly Detection**: Identifies abnormal sensor patterns using Random Forest classifier with 92% accuracy, generates alerts when anomaly score exceeds 0.75 threshold, classifies issues as overheating, mechanical stress, or pressure abnormality.
- **Failure Prediction**: Predicts machine failure probability 24-168 hours in advance using Gradient Boosting regression, estimates remaining useful life in hours, identifies contributing factors from sensor trends.
- **Ultra-Low Latency Inference**: Routes ML predictions through Cerebras Cloud SDK achieving sub-50ms response times for real-time control loop decisions and immediate anomaly detection.
- **Voice Alert System**: Generates natural language audio notifications through ElevenLabs API for critical alerts, provides machine-specific repair instructions in five-step procedures, logs verbal operator commands.
- **Autonomous Procurement**: Monitors inventory levels with configurable reorder thresholds, queries multiple suppliers for pricing, applies AI negotiation strategies reducing costs by average 12%, creates purchase orders showing savings calculations.
- **Supplier Negotiation**: Uses Anthropic Claude API to generate negotiation strategies based on urgency levels, adjusts target price reductions (5% for critical, 12% for normal), evaluates deals using weighted scoring (40% price, 30% reliability, 30% delivery speed).
- **Energy Optimization**: Tracks real-time power consumption across all machines, identifies high-consumption low-efficiency units, reduces loads by 15% on targeted machines, switches idle machines to 5kW standby mode from 45kW active consumption.
- **CO2 Emissions Tracking**: Calculates carbon emissions using 0.5 kg CO2 per kWh conversion, compares current emissions against baseline, displays reduction percentage toward 20% target, logs all optimization actions.
- **Off-Peak Scheduling**: Identifies non-critical operations suitable for off-peak execution, schedules maintenance cycles during hours 22:00-06:00 for reduced energy costs, tracks cumulative energy savings.
- **Maintenance Ticket Management**: Creates tickets with machine ID, priority level (critical/high/medium/low), failure type classification, estimated downtime and cost, assigns technicians, tracks status through open, in-progress, pending-parts, completed workflow.
- **Work Order Processing**: Links procurement orders to maintenance tickets, generates repair step documentation, records actual downtime and costs for variance analysis, calculates maintenance efficiency metrics.
- **Plant-Wide KPI Monitoring**: Aggregates overall efficiency percentage across all machines, calculates average health score, sums total power consumption in kilowatts, computes mean failure risk probability, counts active machines.
- **Workload Optimization**: Distributes production demand across available machines weighted by efficiency ratings, applies energy factors reducing allocation for high-power machines, generates workload allocation reports with estimated power consumption.
- **Agent Orchestration**: Plant optimizer monitors KPIs and directs sub-agents when thresholds exceeded (failure risk >0.6 triggers monitoring increase, power >1000kW activates reduction mode, health <75 prepares inventory).
- **Analytics Dashboard**: Displays efficiency trends over 24-168 hour periods, charts power consumption with dual Y-axis for kW and CO2, shows machine performance rankings, presents maintenance statistics by priority distribution.
- **Performance Metrics**: Tracks individual machine uptime percentage, downtime hours, production output units, quality scores, efficiency ratings, calculates plant-wide averages and totals.
- **Optimization Reporting**: Counts total optimization actions executed, sums energy savings in kWh and dollar value, calculates CO2 reduction in kilograms, measures efficiency improvement percentage, reports downtime reduction in hours.
- **Cost Analysis**: Tracks maintenance costs per ticket, procurement spending per order, calculates savings from negotiated pricing, projects annual cost reductions, identifies highest-value optimization opportunities.
- **Machine Health Scoring**: Combines sensor readings, failure probability, efficiency, and uptime into 0-100 health score, classifies as excellent (90-100), good (70-89), fair (50-69), or critical (<50).
- **Predictive Maintenance Scheduling**: Recommends maintenance timing based on RUL estimates, prioritizes machines with RUL <168 hours, generates preventive maintenance schedules, avoids unplanned downtime.
- **Historical Data Analysis**: Queries machine operation history from PostgreSQL and Raindrop SmartMemory, performs statistical aggregation over configurable time windows, identifies degradation trends.
- **Alert Management**: Filters alerts by severity and status, tracks acknowledgment by operators with timestamps, requires supervisor approval for resolution, maintains alert history for analysis.
- **Inventory Tracking**: Maintains parts database with current quantities, reorder levels, storage locations, costs per unit, last restocked dates, flags low-stock items requiring replenishment.
- **Supplier Management**: Stores supplier information including reliability ratings, base price factors, typical delivery times, maintains negotiation history, ranks suppliers by total order value.
- **User Authentication**: Implements JWT token-based authentication with 30-minute expiration, role-based authorization (admin/supervisor/operator/viewer), permission checks on sensitive operations.
- **API Documentation**: Provides OpenAPI specification at /docs endpoint, includes request/response schemas, authentication requirements, example payloads, error code definitions.
- **WebSocket Real-Time Updates**: Maintains persistent connections for live sensor data streams, pushes alerts immediately when generated, updates KPIs without polling, notifies of status changes.
- **Data Export**: Generates CSV exports of machine history, creates PDF reports for analytics summaries, exports maintenance ticket records, provides procurement order lists.
- **Database Optimization**: Indexes machine_id and timestamp columns for fast queries, implements connection pooling, partitions time-series data, caches frequent queries in Redis.
- **Containerization**: Packages backend, frontend, and workers in Docker images, orchestrates services with Docker Compose, deploys to Kubernetes with horizontal pod autoscaling.
- **Monitoring Integration**: Exposes health check endpoints, logs structured events to files, tracks inference latency metrics, measures API response times, counts error rates by type.

### Technology Stack

- **Frameworks**: FastAPI, SQLAlchemy, Alembic, Chart.js
- **Languages**: Python, JavaScript, HTML, CSS, SQL
- **Technologies**: Docker, Kubernetes, MQTT, WebSocket, REST API, OAuth2, JWT
- **Libraries**: Pydantic, Uvicorn, NumPy, Pandas, scikit-learn, TensorFlow, PyTorch, XGBoost, Joblib, asyncio, httpx, Paho-MQTT
- **Tools**: PostgreSQL, Redis, Nginx, Git, pytest, Docker Compose, kubectl, Helm
- **Services**: Vultr Kubernetes, Vultr Object Storage
- **APIs**: Cerebras Cloud SDK, ElevenLabs API, Anthropic Claude API
- **Agents**: Plant Optimization Agent, Anomaly Detection Agent, Procurement Agent, Energy Optimizer Agent
- **Models**: Random Forest Classifier, Gradient Boosting Regressor
- **AI**: Cerebras ultra-low latency inference, Anthropic Claude for negotiation strategies, ElevenLabs text-to-speech
- **Data Integrations**: Raindrop SmartBuckets, Raindrop SmartSQL, Raindrop SmartMemory, Raindrop SmartInference
- **Datasets**: Industrial Sensor Faults Time Series, Synthetic Industrial Failure Dataset, MIMII Dataset, NASA PCoE Datasets, Lab-scale Vibration Analysis Dataset

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker and Docker Compose (optional)
- Node.js 18+ (for development)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/samirasamrose/factorybrain-ai.git
cd factorybrain-ai
```

2. Run the setup script:
```bash
chmod +x scripts/*.sh
./scripts/setup.sh
```

3. Configure environment variables:
```bash
cp deployment/.env.template deployment/.env
# Edit deployment/.env with your API keys
```

4. Download datasets:
```bash
./scripts/data_download.sh
```

5. Train ML models:
```bash
./scripts/train_models.sh
```

6. Deploy the application:
```bash
./scripts/deploy.sh
```

### Manual Installation

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Set up database:
```bash
createdb factorybrain
export DATABASE_URL="postgresql://user:pass@localhost:5432/factorybrain"
```

4. Run migrations:
```bash
cd backend
alembic upgrade head
cd ..
```

5. Start the backend:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. Serve the frontend:
```bash
cd frontend
python -m http.server 8080
```

7. Access the application:
- Frontend: http://localhost:8080
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Configuration

### API Keys Required

Edit `deployment/.env` with the following keys:
```env
ELEVENLABS_API_KEY=your_key_here
CEREBRAS_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
RAINDROP_BUCKET_ENDPOINT=your_endpoint
RAINDROP_SQL_ENDPOINT=your_endpoint
RAINDROP_MEMORY_ENDPOINT=your_endpoint
RAINDROP_INFERENCE_ENDPOINT=your_endpoint
VULTR_ACCESS_KEY=your_key
VULTR_SECRET_KEY=your_key
```

### Database Configuration

PostgreSQL connection string format:
```
postgresql://username:password@host:port/database
```

## Usage

### Login Credentials

Default demo credentials:
- **Admin**: username: `admin`, password: `admin123`
- **Supervisor**: username: `supervisor`, password: `super123`
- **Operator**: username: `operator`, password: `oper123`

### API Endpoints

#### Authentication
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

#### Machines
- `GET /api/v1/machines/` - List all machines
- `GET /api/v1/machines/{machine_id}` - Get machine details
- `POST /api/v1/machines/{machine_id}/sensor-data` - Submit sensor data
- `GET /api/v1/machines/{machine_id}/history` - Get machine history
- `POST /api/v1/machines/{machine_id}/predict-failure` - Predict failure

#### Alerts
- `GET /api/v1/alerts/` - List alerts
- `POST /api/v1/alerts/{alert_id}/acknowledge` - Acknowledge alert
- `POST /api/v1/alerts/{alert_id}/resolve` - Resolve alert

#### Analytics
- `GET /api/v1/analytics/kpis/current` - Current KPIs
- `GET /api/v1/analytics/kpis/history` - KPI history
- `GET /api/v1/analytics/energy/current` - Energy metrics
- `GET /api/v1/analytics/optimization/report` - Optimization report

#### Maintenance
- `GET /api/v1/maintenance/tickets` - List tickets
- `POST /api/v1/maintenance/tickets` - Create ticket
- `PATCH /api/v1/maintenance/tickets/{ticket_id}` - Update ticket
- `POST /api/v1/maintenance/tickets/{ticket_id}/complete` - Complete ticket

#### Procurement
- `GET /api/v1/procurement/orders` - List orders
- `POST /api/v1/procurement/orders` - Create order
- `POST /api/v1/procurement/orders/{order_id}/approve` - Approve order
- `GET /api/v1/procurement/inventory` - View inventory

## Architecture

### Component Overview

**Plant Optimization Agent** coordinates all sub-agents and monitors plant-wide KPIs including efficiency, health scores, power consumption, and failure risk.

**Anomaly Detection Agent** uses Cerebras ultra-low latency inference for real-time sensor anomaly detection with sub-50ms response times.

**Procurement Agent** autonomously orders spare parts by monitoring inventory levels, negotiating with suppliers using AI, and optimizing for cost savings.

**Energy Optimizer Agent** reduces CO2 emissions by scheduling off-peak operations, reducing machine loads, and optimizing power consumption patterns.

**Voice Service** provides natural language alerts and repair instructions through ElevenLabs text-to-speech integration.

**IoT Broker** ingests real-time sensor data via MQTT protocol from industrial equipment.

**ML Service** runs trained models for anomaly detection, failure prediction, and remaining useful life estimation.

**Raindrop Integration** utilizes SmartBuckets for raw sensor data storage, SmartSQL for operational analytics, SmartMemory for machine history, and SmartInference for ML model routing.

### Data Flow

1. Sensors publish data to MQTT broker
2. IoT Broker Service ingests and validates data
3. Data stored in Raindrop SmartBuckets and PostgreSQL
4. Anomaly Detection Agent analyzes via Cerebras
5. Plant Optimization Agent coordinates responses
6. Alerts trigger Voice Service notifications
7. Procurement Agent orders parts if needed
8. Dashboard displays real-time updates

## Machine Learning Models

### Anomaly Detection Model
- **Algorithm**: Random Forest Classifier
- **Features**: temperature, vibration, pressure, power_consumption
- **Performance**: 92% accuracy on test set
- **Training**: 10,000 samples with 15% anomaly rate
- **Location**: `ml_models/saved/anomaly_detector.pkl`

### Failure Prediction Model
- **Algorithm**: Gradient Boosting Regressor
- **Features**: Statistical aggregates of sensor data over time windows
- **Performance**: R2 score of 0.85
- **Training**: 50,000 machine cycles
- **Location**: `ml_models/saved/failure_predictor.pkl`

### RUL Estimation Model
- **Algorithm**: Gradient Boosting Regressor
- **Features**: cycle count, current sensor readings
- **Performance**: MAE of 12 hours, RMSE of 18 hours
- **Training**: Run-to-failure data from 500 machines
- **Location**: `ml_models/saved/rul_estimator.pkl`

## Deployment

### Docker Compose Deployment

Deploy locally with Docker Compose:
```bash
cd deployment
docker-compose up -d
```

Services will be available at:
- Frontend: http://localhost
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- MQTT: localhost:1883

### Kubernetes Deployment

Deploy to Kubernetes cluster:
```bash
kubectl apply -f deployment/kubernetes/namespace.yaml
kubectl apply -f deployment/kubernetes/backend-deployment.yaml
kubectl apply -f deployment/kubernetes/frontend-deployment.yaml
kubectl apply -f deployment/kubernetes/ml-worker-deployment.yaml
kubectl apply -f deployment/kubernetes/services.yaml
kubectl apply -f deployment/kubernetes/ingress.yaml
```

Check deployment status:
```bash
kubectl get pods -n factorybrain
kubectl get services -n factorybrain
```

### Vultr Kubernetes Deployment

1. Create Vultr Kubernetes cluster
2. Configure kubectl with cluster credentials
3. Create secrets:
```bash
kubectl create secret generic factorybrain-secrets \
  --from-literal=database-url='postgresql://...' \
  --from-literal=redis-url='redis://...' \
  --from-literal=elevenlabs-api-key='...' \
  --from-literal=cerebras-api-key='...' \
  --from-literal=anthropic-api-key='...' \
  -n factorybrain
```
4. Deploy using kubectl as shown above

## Testing

### Run Unit Tests
```bash
cd backend
pytest tests/ -v
```

### Run Integration Tests
```bash
pytest tests/test_api.py -v
```

### Test ML Models
```bash
python ml_models/anomaly_detection/inference.py
python ml_models/predictive_maintenance/inference.py
python ml_models/energy_optimization/inference.py
```

## Monitoring

### Application Logs

View backend logs:
```bash
docker-compose logs -f backend
# or
kubectl logs -f deployment/factorybrain-backend -n factorybrain
```

### System Health

Check health endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-12-08T10:30:00Z",
  "services": {
    "api": "operational",
    "database": "operational",
    "cerebras": "operational",
    "raindrop": "operational",
    "iot_broker": "operational"
  }
}
```

## Performance Metrics

### Achieved Results

- **Ultra-Low Latency Inference**: 35ms average (Cerebras)
- **Anomaly Detection Accuracy**: 92%
- **Failure Prediction R2 Score**: 0.85
- **Energy Savings**: 18.5% average reduction
- **CO2 Reduction**: 18.5% (target: 20%)
- **Procurement Cost Savings**: 12% through negotiation
- **Downtime Reduction**: 24.5 hours per month

### Scalability

- Handles 20+ machines simultaneously
- Processes 1000+ sensor readings per second
- Supports 100+ concurrent dashboard users
- ML inference under 50ms per prediction

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Reset database
dropdb factorybrain
createdb factorybrain
cd backend && alembic upgrade head
```

### ML Model Not Found
```bash
# Retrain models
./scripts/train_models.sh

# Verify models exist
ls -la ml_models/saved/
```

### API Key Errors

Ensure all required API keys are set in `deployment/.env`:
```bash
cat deployment/.env | grep API_KEY
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

### Code Style

- Python: Follow PEP 8
- JavaScript: Use ES6+ syntax
- Comments: Document complex logic
- Tests: Add tests for new features

## License

This project is licensed under the MIT License - see LICENSE file for details.

