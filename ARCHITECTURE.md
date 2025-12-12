# FactoryBrain AI - Architecture Documentation

## System Overview

FactoryBrain AI is a distributed, multi-agent system designed for autonomous industrial process optimization. The architecture follows microservices principles with event-driven communication patterns.

## High-Level Architecture

┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Dashboard │  │ Machines │  │Analytics │  │Maintenance│  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└────────────────────────┬────────────────────────────────────┘
│ HTTPS/WSS
┌────────────────────────┴────────────────────────────────────┐
│                     API Gateway Layer                        │
│              FastAPI + WebSocket Server                      │
└────────────────────────┬────────────────────────────────────┘
│
┌────────────────────────┴────────────────────────────────────┐
│                   Agent Orchestration Layer                  │
│  ┌────────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │Plant Optimizer │  │   Anomaly    │  │  Procurement   │ │
│  │     Agent      │  │   Detector   │  │     Agent      │ │
│  └────────────────┘  └──────────────┘  └────────────────┘ │
│  ┌────────────────┐  ┌──────────────┐                      │
│  │     Energy     │  │    Voice     │                      │
│  │   Optimizer    │  │   Service    │                      │
│  └────────────────┘  └──────────────┘                      │
└────────────────────────┬────────────────────────────────────┘
│
┌────────────────────────┴────────────────────────────────────┐
│                   Service Layer                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Cerebras │  │ElevenLabs│  │ Raindrop │  │   MQTT   │  │
│  │   SDK    │  │   API    │  │   Smart  │  │  Broker  │  │
│  │          │  │          │  │Components│  │          │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└────────────────────────┬────────────────────────────────────┘
│
┌────────────────────────┴────────────────────────────────────┐
│                   Data Layer                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │PostgreSQL│  │  Redis   │  │  Vultr   │  │    ML    │     │
│  │  Cache   │  │  Object  │  │  Models  │  │  Storage │     │         
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────┘

## Component Architecture

### Frontend Architecture

**Technology Stack**:
- HTML5, CSS3, JavaScript (ES6+)
- Chart.js for visualizations
- Native WebSocket for real-time updates
- Responsive design for mobile/tablet

**Key Components**:
- **Dashboard**: Real-time plant overview with KPIs
- **Machine Monitor**: Detailed machine status and history
- **Analytics**: Advanced reporting and visualizations
- **Maintenance**: Ticket and procurement management

**State Management**:
- LocalStorage for authentication tokens
- In-memory state for real-time updates
- WebSocket subscriptions for live data

### Backend Architecture

**Technology Stack**:
- FastAPI for REST API
- Python 3.11 with async/await
- SQLAlchemy ORM
- Pydantic for validation

**API Layer**:
```python
backend/app/api/
├── dependencies.py    # Auth, DB session injection
├── routes/
│   ├── machines.py    # Machine management
│   ├── alerts.py      # Alert handling
│   ├── analytics.py   # KPI and reporting
│   ├── maintenance.py # Ticket management
│   └── procurement.py # Procurement orders
```

**Agent Layer**:
```python
backend/app/agents/
├── plant_optimizer.py    # Main orchestrator
├── anomaly_detector.py   # Fault detection
├── procurement_agent.py  # Autonomous ordering
└── energy_optimizer.py   # CO2 reduction
```

**Service Layer**:
```python
backend/app/services/
├── voice_service.py      # ElevenLabs integration
├── cerebras_service.py   # Ultra-low latency ML
├── raindrop_service.py   # SmartComponents
├── ml_service.py         # Local ML models
└── iot_broker.py         # MQTT communication
```

### Agent Architecture

#### Plant Optimization Agent

**Responsibilities**:
- Monitor plant-wide KPIs
- Coordinate sub-agents
- Optimize workload distribution
- Generate optimization reports

**Decision Logic**:
1. Collect KPIs from all machines
2. Identify optimization opportunities
3. Direct sub-agents to take action
4. Track results and adjust

**Communication Pattern**:
- Plant Optimizer → Anomaly Detector: "Increase monitoring frequency"
- Plant Optimizer → Energy Optimizer: "Activate reduction mode"
- Plant Optimizer → Procurement Agent: "Prepare spare parts inventory"

#### Anomaly Detection Agent

**Responsibilities**:
- Real-time sensor analysis
- Failure prediction
- Vibration pattern detection
- Alert generation

**Detection Pipeline**:
1. Receive sensor data from IoT Broker
2. Extract features and normalize
3. Run Cerebras ultra-low latency inference
4. Classify anomaly type
5. Trigger alerts if threshold exceeded

**Performance Requirements**:
- Inference latency: < 50ms
- Detection accuracy: > 90%
- False positive rate: < 5%

#### Procurement Agent

**Responsibilities**:
- Inventory monitoring
- Supplier negotiation
- Autonomous ordering
- Cost optimization

**Negotiation Strategy**:
1. Find suppliers for required part
2. Get initial quotes
3. Use AI to generate negotiation strategy
4. Apply target reduction based on urgency
5. Select best deal based on price, reliability, delivery

**Savings Calculation**:
```python
savings = (quoted_price - negotiated_price) * quantity
deal_score = price_savings * 0.4 + reliability * 0.3 + delivery_speed * 0.3
```

#### Energy Optimizer Agent

**Responsibilities**:
- Power consumption monitoring
- CO2 emissions tracking
- Load reduction strategies
- Off-peak scheduling

**Optimization Actions**:
1. Reduce load on high-power, low-efficiency machines
2. Switch idle machines to standby mode
3. Schedule non-critical operations off-peak
4. Track savings against baseline

**CO2 Calculation**:
```python
co2_emissions_kg = total_power_kw * 0.5
reduction_percentage = (baseline - current) / baseline * 100
```

### Data Architecture

#### Database Schema

**Machines Table**:
- Primary data: machine_id, name, type, location
- Status: status, health_score, is_active
- Sensors: temperature, vibration, pressure, power_consumption
- Predictions: failure_probability, remaining_useful_life
- Maintenance: last_maintenance, next_maintenance

**Sensor Readings Table**:
- machine_id (indexed)
- sensor_type, value, unit
- timestamp (indexed)
- is_anomaly, anomaly_score

**Maintenance Tickets Table**:
- ticket_id, machine_id
- title, description, status, priority
- assigned_to, reported_by
- failure_type, repair_steps
- cost_estimate, actual_cost
- timestamps

**Procurement Orders Table**:
- order_id, part_name, part_number
- supplier, quantity
- unit_price, negotiated_price, savings
- status, urgency
- estimated_delivery, actual_delivery

#### Data Flow

**Sensor Data Ingestion**:

IoT Device → MQTT Broker → IoT Service → PostgreSQL + Raindrop
↓
Anomaly Detector
↓
Alert Generation

**Real-time Updates**:

Database Change → Event Trigger → WebSocket → Frontend Update

**Analytics Pipeline**:

Raw Sensor Data → Feature Engineering → ML Models → Predictions
↓
Raindrop SmartSQL → Analytics API → Dashboard Visualizations

### ML Architecture

#### Model Pipeline

**Training Pipeline**:
1. Load datasets from multiple sources
2. Preprocess and feature engineering
3. Train models with hyperparameter tuning
4. Validate performance metrics
5. Save models to ml_models/saved/

**Inference Pipeline**:
1. Receive input features
2. Load cached model from memory
3. Scale features using saved scaler
4. Run prediction
5. Post-process and return result

**Model Serving**:
- Local models: Joblib pickle files
- Cerebras models: API calls for ultra-low latency
- Raindrop SmartInference: Routing layer

#### Feature Engineering

**Anomaly Detection Features**:
- Raw sensor values (temperature, vibration, pressure, power)
- Rolling statistics (mean, std, max, min)
- Outlier detection using z-scores

**Failure Prediction Features**:
- Statistical aggregates over time windows
- Trend detection (increasing temperature, vibration)
- Threshold crossing counts
- Cycle counts and cumulative stress

**RUL Estimation Features**:
- Current cycle number
- Current sensor readings
- Degradation rate from historical data
- Maintenance history

### Integration Architecture

#### Cerebras Integration

**Purpose**: Ultra-low latency inference for real-time decisions

**Usage Pattern**:
```python
response = await cerebras_service.inference_request({
    "model": "anomaly_detector_v1",
    "inputs": sensor_features,
    "ultra_low_latency": True,
    "max_latency_ms": 50
})
```

**Performance Monitoring**:
- Track latency per request
- Calculate average latency
- Alert if latency exceeds threshold

#### Raindrop Integration

**SmartBuckets**: Store raw sensor data with automatic partitioning
**SmartSQL**: Query operational data with optimized indexes
**SmartMemory**: Store machine learning history and context
**SmartInference**: Route ML requests to optimal compute

**Data Storage Pattern**:
```python
await raindrop.store_sensor_data(machine_id, {
    "temperature": 75.5,
    "vibration": 0.42,
    "timestamp": datetime.utcnow()
})
```

#### ElevenLabs Integration

**Purpose**: Natural language voice alerts for operators

**Alert Generation**:
```python
await voice_service.alert_machine_overheating(
    machine_id="M014",
    temperature=95.0
)
# Output: "Machine M014 bearings overheating. 
#          Current temperature: 95 degrees Celsius."
```

**Repair Instructions**:
- Generate step-by-step voice guidance
- Adjust tone based on severity
- Log all voice interactions

#### Vultr Integration

**Kubernetes**: Run containerized workloads at edge locations
**Object Storage**: Store sensor logs and model artifacts
**Network**: Low-latency connections to factory floor

### Security Architecture

#### Authentication Flow

1. User submits credentials
2. Backend validates against database
3. Generate JWT token with expiration
4. Return token to frontend
5. Frontend includes token in all requests
6. Backend validates token on each request

#### Authorization Model

**Role Hierarchy**:
- **Admin**: Full system access
- **Supervisor**: Approve orders, assign tickets
- **Operator**: View data, create tickets
- **Viewer**: Read-only access

**Permission Checks**:
```python
@router.post("/orders/{order_id}/approve")
async def approve_order(
    order_id: str,
    current_user = Depends(require_supervisor)
):
    # Only supervisors and admins can approve
```

#### Data Security

- Database credentials stored in environment variables
- API keys encrypted at rest
- TLS/SSL for all external communications
- Rate limiting to prevent abuse
- Input validation using Pydantic

### Scalability Architecture

#### Horizontal Scaling

**Stateless Services**:
- Backend API servers
- ML workers
- WebSocket servers

**Load Balancing**:
- Kubernetes service load balancing
- Round-robin for API requests
- Sticky sessions for WebSocket

#### Vertical Scaling

**Resource Allocation**:
- Backend: 512MB-2GB memory, 0.5-2 CPU
- ML Workers: 1-4GB memory, 1-2 CPU
- Database: 4-16GB memory, 2-4 CPU

#### Caching Strategy

**Redis Caching**:
- KPI calculations (TTL: 60s)
- Machine status (TTL: 30s)
- User sessions
- ML model predictions (TTL: 300s)

**Application-Level Caching**:
- Loaded ML models in memory
- Database connection pools
- Static file caching

### Monitoring Architecture

#### Application Metrics

- Request rate and latency
- Error rates and types
- ML inference latency
- Database query performance

#### Business Metrics

- Machine health scores
- Energy consumption
- CO2 reduction percentage
- Procurement savings
- Downtime hours

#### Alerting

**Critical Alerts**:
- Service down
- Database connection lost
- ML model failure
- High error rate

**Warning Alerts**:
- High latency (>500ms)
- Low health scores (<70)
- High failure risk (>0.7)

### Deployment Architecture

#### Local Development

Docker Compose
├── PostgreSQL container
├── Redis container
├── MQTT broker container
├── Backend container (hot reload)
└── Frontend container (nginx)

#### Production Kubernetes

Kubernetes Cluster (Vultr)
├── factorybrain namespace
│   ├── backend-deployment (3 replicas)
│   ├── frontend-deployment (2 replicas)
│   ├── ml-worker-deployment (2 replicas)
│   ├── postgres statefulset (1 replica)
│   └── redis deployment (1 replica)
├── Services
│   ├── backend-service (ClusterIP)
│   ├── frontend-service (LoadBalancer)
│   ├── postgres-service (ClusterIP)
│   └── redis-service (ClusterIP)
└── Ingress (HTTPS termination)

#### CI/CD Pipeline

1. Code commit to GitHub
2. Run automated tests
3. Build Docker images
4. Push to container registry
5. Update Kubernetes manifests
6. Rolling deployment
7. Health checks
8. Rollback if needed

## Performance Optimization

### Database Optimization

- Indexes on frequently queried columns
- Connection pooling
- Query result caching
- Partitioning for time-series data

### API Optimization

- Async/await for I/O operations
- Background tasks for heavy processing
- Response compression
- Pagination for large results

### Frontend Optimization

- Lazy loading for charts
- Debouncing for search inputs
- WebSocket for real-time updates
- Service worker for offline support

## Disaster Recovery

### Backup Strategy

- Database: Daily automated backups
- ML Models: Versioned in object storage
- Logs: 30-day retention
- Configuration: Version controlled

### Failover Strategy

- Multi-zone Kubernetes deployment
- Database replication
- Redis sentinel for high availability
- Automatic pod restart on failure

## Future Enhancements

1. GraphQL API for flexible queries
2. Machine learning model versioning
3. Multi-tenant support
4. Mobile app with offline capabilities
5. Advanced predictive analytics
6. Integration with ERP systems