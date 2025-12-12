from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/machines", tags=["machines"])

class MachineResponse(BaseModel):
    id: int
    machine_id: str
    name: str
    type: str
    location: str
    status: str
    health_score: float
    temperature: Optional[float]
    vibration: Optional[float]
    pressure: Optional[float]
    power_consumption: Optional[float]
    efficiency: Optional[float]
    failure_probability: Optional[float]
    remaining_useful_life: Optional[float]
    last_maintenance: Optional[datetime]
    next_maintenance: Optional[datetime]

class SensorDataInput(BaseModel):
    machine_id: str
    temperature: float
    vibration: float
    pressure: float
    power_consumption: float

class MachineStatusUpdate(BaseModel):
    status: str
    health_score: Optional[float]

@router.get("/", response_model=List[MachineResponse])
async def get_all_machines(
    status: Optional[str] = Query(None),
    min_health: Optional[float] = Query(None),
    current_user = Depends(get_current_active_user)
):
    machines = []
    
    for i in range(1, 21):
        machine = MachineResponse(
            id=i,
            machine_id=f"M{i:03d}",
            name=f"Machine {i}",
            type="production" if i % 3 != 0 else "assembly",
            location=f"Zone {(i-1)//5 + 1}",
            status="operational" if i % 7 != 0 else "maintenance",
            health_score=85.0 + (i % 15),
            temperature=65.0 + (i % 20),
            vibration=0.3 + (i % 10) * 0.05,
            pressure=55.0 + (i % 15),
            power_consumption=40.0 + (i % 30),
            efficiency=80.0 + (i % 15),
            failure_probability=0.1 + (i % 10) * 0.05,
            remaining_useful_life=500.0 + (i * 100),
            last_maintenance=datetime.utcnow(),
            next_maintenance=datetime.utcnow()
        )
        
        if status and machine.status != status:
            continue
        if min_health and machine.health_score < min_health:
            continue
        
        machines.append(machine)
    
    return machines

@router.get("/{machine_id}", response_model=MachineResponse)
async def get_machine(
    machine_id: str,
    current_user = Depends(get_current_active_user)
):
    machine_num = int(machine_id.replace('M', ''))
    
    return MachineResponse(
        id=machine_num,
        machine_id=machine_id,
        name=f"Machine {machine_num}",
        type="production",
        location=f"Zone {(machine_num-1)//5 + 1}",
        status="operational",
        health_score=92.5,
        temperature=68.5,
        vibration=0.42,
        pressure=58.3,
        power_consumption=48.7,
        efficiency=88.5,
        failure_probability=0.15,
        remaining_useful_life=720.0,
        last_maintenance=datetime.utcnow(),
        next_maintenance=datetime.utcnow()
    )

@router.post("/{machine_id}/sensor-data")
async def post_sensor_data(
    machine_id: str,
    sensor_data: SensorDataInput,
    current_user = Depends(get_current_active_user)
):
    return {
        "machine_id": machine_id,
        "data_received": sensor_data.dict(),
        "timestamp": datetime.utcnow().isoformat(),
        "status": "processed"
    }

@router.patch("/{machine_id}/status")
async def update_machine_status(
    machine_id: str,
    status_update: MachineStatusUpdate,
    current_user = Depends(require_supervisor)
):
    return {
        "machine_id": machine_id,
        "old_status": "operational",
        "new_status": status_update.status,
        "updated_at": datetime.utcnow().isoformat()
    }

@router.get("/{machine_id}/history")
async def get_machine_history(
    machine_id: str,
    hours: int = Query(24, ge=1, le=168),
    current_user = Depends(get_current_active_user)
):
    history = []
    for i in range(hours):
        history.append({
            "timestamp": (datetime.utcnow() - timedelta(hours=hours-i)).isoformat(),
            "temperature": 65.0 + np.random.normal(0, 5),
            "vibration": 0.4 + np.random.normal(0, 0.1),
            "pressure": 60.0 + np.random.normal(0, 5),
            "power_consumption": 50.0 + np.random.normal(0, 10),
            "health_score": 90.0 + np.random.normal(0, 5)
        })
    
    return {
        "machine_id": machine_id,
        "period_hours": hours,
        "data_points": len(history),
        "history": history
    }

@router.post("/{machine_id}/predict-failure")
async def predict_machine_failure(
    machine_id: str,
    current_user = Depends(get_current_active_user)
):
    failure_prob = np.random.uniform(0.1, 0.9)
    
    return {
        "machine_id": machine_id,
        "failure_probability": failure_prob,
        "risk_level": "critical" if failure_prob > 0.7 else "medium" if failure_prob > 0.4 else "low",
        "estimated_time_to_failure_hours": 168 * (1 - failure_prob),
        "contributing_factors": ["high_temperature", "vibration_anomaly"],
        "timestamp": datetime.utcnow().isoformat()
    }
