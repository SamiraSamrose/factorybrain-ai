# FactoryBrain AI - API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints (except login) require Bearer token authentication.

### Login

**Endpoint**: `POST /auth/login`

**Request Body**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "username": "admin",
    "role": "admin",
    "full_name": "Administrator"
  }
}
```

### Using Authentication

Include the token in the Authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Machines Endpoints

### List All Machines

**Endpoint**: `GET /api/v1/machines/`

**Query Parameters**:
- `status` (optional): Filter by status (operational, maintenance, standby, offline)
- `min_health` (optional): Minimum health score (0-100)

**Response**:
```json
[
  {
    "id": 1,
    "machine_id": "M001",
    "name": "Machine 1",
    "type": "production",
    "location": "Zone 1",
    "status": "operational",
    "health_score": 92.5,
    "temperature": 68.5,
    "vibration": 0.42,
    "pressure": 58.3,
    "power_consumption": 48.7,
    "efficiency": 88.5,
    "failure_probability": 0.15,
    "remaining_useful_life": 720.0,
    "last_maintenance": "2024-12-01T10:00:00Z",
    "next_maintenance": "2025-01-01T10:00:00Z"
  }
]
```

### Get Machine Details

**Endpoint**: `GET /api/v1/machines/{machine_id}`

**Response**: Single machine object (same structure as list)

### Submit Sensor Data

**Endpoint**: `POST /api/v1/machines/{machine_id}/sensor-data`

**Request Body**:
```json
{
  "machine_id": "M001",
  "temperature": 75.5,
  "vibration": 0.45,
  "pressure": 60.0,
  "power_consumption": 52.0
}
```

**Response**:
```json
{
  "machine_id": "M001",
  "data_received": {
    "temperature": 75.5,
    "vibration": 0.45,
    "pressure": 60.0,
    "power_consumption": 52.0
  },
  "timestamp": "2024-12-08T10:30:00Z",
  "status": "processed"
}
```

### Get Machine History

**Endpoint**: `GET /api/v1/machines/{machine_id}/history`

**Query Parameters**:
- `hours` (default: 24, max: 168): Hours of history to retrieve

**Response**:
```json
{
  "machine_id": "M001",
  "period_hours": 24,
  "data_points": 24,
  "history": [
    {
      "timestamp": "2024-12-08T09:00:00Z",
      "temperature": 68.5,
      "vibration": 0.42,
      "pressure": 58.3,
      "power_consumption": 48.7,
      "health_score": 92.5
    }
  ]
}
```

### Predict Machine Failure

**Endpoint**: `POST /api/v1/machines/{machine_id}/predict-failure`

**Response**:
```json
{
  "machine_id": "M001",
  "failure_probability": 0.25,
  "risk_level": "low",
  "estimated_time_to_failure_hours": 540.0,
  "contributing_factors": ["high_temperature", "vibration_anomaly"],
  "timestamp": "2024-12-08T10:30:00Z"
}
```

## Alerts Endpoints

### List Alerts

**Endpoint**: `GET /api/v1/alerts/`

**Query Parameters**:
- `severity` (optional): critical, high, medium, low
- `machine_id` (optional): Filter by machine
- `resolved` (optional): true/false
- `limit` (default: 50, max: 500)

**Response**:
```json
[
  {
    "id": 1,
    "alert_type": "overheating",
    "machine_id": "M014",
    "severity": "critical",
    "message": "Machine M014 bearings overheating",
    "timestamp": "2024-12-08T10:25:00Z",
    "acknowledged": false,
    "acknowledged_by": null,
    "resolved": false
  }
]
```

### Acknowledge Alert

**Endpoint**: `POST /api/v1/alerts/{alert_id}/acknowledge`

**Request Body**:
```json
{
  "acknowledged_by": "operator_1",
  "notes": "Inspecting machine now"
}
```

**Response**:
```json
{
  "alert_id": 1,
  "acknowledged": true,
  "acknowledged_by": "operator_1",
  "acknowledged_at": "2024-12-08T10:30:00Z",
  "notes": "Inspecting machine now"
}
```

### Resolve Alert

**Endpoint**: `POST /api/v1/alerts/{alert_id}/resolve`

**Request Body**:
```json
{
  "resolution_notes": "Bearings replaced, machine operational"
}
```

**Requires**: Supervisor or Admin role

## Analytics Endpoints

### Current KPIs

**Endpoint**: `GET /api/v1/analytics/kpis/current`

**Response**:
```json
{
  "timestamp": "2024-12-08T10:30:00Z",
  "overall_efficiency": 87.5,
  "average_health": 89.3,
  "total_power_consumption": 945.7,
  "failure_risk": 0.23,
  "active_machines": 18
}
```

### KPI History

**Endpoint**: `GET /api/v1/analytics/kpis/history`

**Query Parameters**:
- `hours` (default: 24, max: 168)

**Response**: Array of KPI objects with timestamps

### Energy Metrics

**Endpoint**: `GET /api/v1/analytics/energy/current`

**Response**:
```json
{
  "timestamp": "2024-12-08T10:30:00Z",
  "total_power_kw": 945.7,
  "average_power_kw": 52.5,
  "estimated_co2_kg": 472.85,
  "active_machines": 18,
  "co2_reduction_percentage": 18.5
}
```

### Optimization Report

**Endpoint**: `GET /api/v1/analytics/optimization/report`

**Response**:
```json
{
  "timestamp": "2024-12-08T10:30:00Z",
  "optimization_actions": 47,
  "energy_savings_kwh": 2847.5,
  "cost_savings": 12450.75,
  "co2_reduction_kg": 1423.75,
  "efficiency_improvement": 8.5,
  "downtime_reduction_hours": 24.5,
  "top_optimizations": [
    {
      "action": "workload_redistribution",
      "count": 15,
      "impact": "high"
    }
  ],
  "recommendations": [
    "Continue energy optimization during off-peak hours"
  ]
}
```

## Maintenance Endpoints

### List Tickets

**Endpoint**: `GET /api/v1/maintenance/tickets`

**Query Parameters**:
- `status` (optional): open, in_progress, pending_parts, completed
- `priority` (optional): critical, high, medium, low
- `machine_id` (optional)
- `limit` (default: 50, max: 200)

**Response**: Array of ticket objects

### Create Ticket

**Endpoint**: `POST /api/v1/maintenance/tickets`

**Request Body**:
```json
{
  "machine_id": "M014",
  "title": "Bearing overheating issue",
  "description": "Machine M014 bearings showing signs of overheating",
  "priority": "high",
  "failure_type": "overheating"
}
```

**Response**: Created ticket object

### Assign Ticket

**Endpoint**: `POST /api/v1/maintenance/tickets/{ticket_id}/assign`

**Request Body**:
```json
{
  "technician": "technician_2"
}
```

**Requires**: Supervisor or Admin role

### Complete Ticket

**Endpoint**: `POST /api/v1/maintenance/tickets/{ticket_id}/complete`

**Request Body**:
```json
{
  "completion_notes": "Bearings replaced successfully",
  "actual_downtime": 4.5,
  "actual_cost": 2200.0
}
```

## Procurement Endpoints

### List Orders

**Endpoint**: `GET /api/v1/procurement/orders`

**Query Parameters**:
- `status` (optional): requested, negotiating, ordered, shipped, delivered
- `urgency` (optional): critical, high, medium, low
- `limit` (default: 50, max: 200)

**Response**: Array of procurement order objects

### Create Order

**Endpoint**: `POST /api/v1/procurement/orders`

**Request Body**:
```json
{
  "part_name": "Bearing Assembly",
  "part_number": "PN-45678",
  "quantity": 5,
  "urgency": "high",
  "machine_id": "M014",
  "ticket_id": "MT-20241207001"
}
```

**Response**:
```json
{
  "id": 1,
  "order_id": "PO-20241208103000",
  "part_name": "Bearing Assembly",
  "part_number": "PN-45678",
  "quantity": 5,
  "supplier": "Industrial Parts Co",
  "unit_price": 250.0,
  "total_price": 1250.0,
  "negotiated_price": 220.0,
  "savings": 150.0,
  "status": "requested",
  "urgency": "high",
  "estimated_delivery": "2024-12-11T10:30:00Z",
  "created_at": "2024-12-08T10:30:00Z"
}
```

### Approve Order

**Endpoint**: `POST /api/v1/procurement/orders/{order_id}/approve`

**Requires**: Supervisor or Admin role

**Response**:
```json
{
  "order_id": "PO-20241208103000",
  "status": "ordered",
  "approved_by": "supervisor_1",
  "approved_at": "2024-12-08T10:35:00Z"
}
```

### View Inventory

**Endpoint**: `GET /api/v1/procurement/inventory`

**Query Parameters**:
- `low_stock_only` (optional): true/false

**Response**: Array of inventory items

## Error Responses

All endpoints may return these error responses:

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

API endpoints are rate limited to:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated requests

Rate limit headers included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1702035000
```

## Pagination

List endpoints support pagination:

**Query Parameters**:
- `skip` (default: 0): Number of records to skip
- `limit` (default: 50): Maximum records to return

**Response Headers**:
```
X-Total-Count: 250
X-Page: 1
X-Per-Page: 50
```

## WebSocket API

Real-time updates via WebSocket:

**Endpoint**: `ws://localhost:8000/ws?token={access_token}`

**Message Types**:
- `sensor_update`: Real-time sensor data
- `alert`: New alerts
- `kpi_update`: KPI changes

**Example Message**:
```json
{
  "type": "alert",
  "data": {
    "machine_id": "M014",
    "severity": "critical",
    "message": "Machine M014 bearings overheating",
    "timestamp": "2024-12-08T10:30:00Z"
  }
}
