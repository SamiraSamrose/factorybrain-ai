from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel
import numpy as np

router = APIRouter(prefix="/analytics", tags=["analytics"])

class KPIResponse(BaseModel):
    timestamp: datetime
    overall_efficiency: float
    average_health: float
    total_power_consumption: float
    failure_risk: float
    active_machines: int

class EnergyMetrics(BaseModel):
    timestamp: datetime
    total_power_kw: float
    average_power_kw: float
    estimated_co2_kg: float
    active_machines: int
    co2_reduction_percentage: float

@router.get("/kpis/current", response_model=KPIResponse)
async def get_current_kpis(
    current_user = Depends(get_current_active_user)
):
    return KPIResponse(
        timestamp=datetime.utcnow(),
        overall_efficiency=87.5,
        average_health=89.3,
        total_power_consumption=945.7,
        failure_risk=0.23,
        active_machines=18
    )

@router.get("/kpis/history", response_model=List[KPIResponse])
async def get_kpi_history(
    hours: int = Query(24, ge=1, le=168),
    current_user = Depends(get_current_active_user)
):
    history = []
    
    for i in range(hours):
        timestamp = datetime.utcnow() - timedelta(hours=hours-i)
        
        history.append(KPIResponse(
            timestamp=timestamp,
            overall_efficiency=85.0 + np.random.normal(2, 3),
            average_health=88.0 + np.random.normal(2, 4),
            total_power_consumption=900.0 + np.random.normal(50, 50),
            failure_risk=0.2 + np.random.normal(0.05, 0.1),
            active_machines=18 + np.random.randint(-2, 3)
        ))
    
    return history

@router.get("/energy/current", response_model=EnergyMetrics)
async def get_current_energy_metrics(
    current_user = Depends(get_current_active_user)
):
    total_power = 945.7
    
    return EnergyMetrics(
        timestamp=datetime.utcnow(),
        total_power_kw=total_power,
        average_power_kw=total_power / 18,
        estimated_co2_kg=total_power * 0.5,
        active_machines=18,
        co2_reduction_percentage=18.5
    )

@router.get("/energy/history", response_model=List[EnergyMetrics])
async def get_energy_history(
    hours: int = Query(24, ge=1, le=168),
    current_user = Depends(get_current_active_user)
):
    history = []
    
    for i in range(hours):
        timestamp = datetime.utcnow() - timedelta(hours=hours-i)
        total_power = 900.0 + np.random.normal(50, 50)
        active = 18 + np.random.randint(-2, 3)
        
        history.append(EnergyMetrics(
            timestamp=timestamp,
            total_power_kw=total_power,
            average_power_kw=total_power / active if active > 0 else 0,
            estimated_co2_kg=total_power * 0.5,
            active_machines=active,
            co2_reduction_percentage=15.0 + np.random.normal(3, 2)
        ))
    
    return history

@router.get("/performance/machines")
async def get_machine_performance(
    current_user = Depends(get_current_active_user)
):
    machines = []
    
    for i in range(1, 21):
        machines.append({
            "machine_id": f"M{i:03d}",
            "efficiency": 80.0 + np.random.normal(5, 8),
            "uptime_percentage": 90.0 + np.random.normal(5, 5),
            "downtime_hours": np.random.uniform(0.5, 5),
            "production_output": np.random.randint(800, 1200),
            "quality_score": 95.0 + np.random.normal(2, 3)
        })
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "machines": machines,
        "summary": {
            "average_efficiency": np.mean([m["efficiency"] for m in machines]),
            "average_uptime": np.mean([m["uptime_percentage"] for m in machines]),
            "total_production": sum([m["production_output"] for m in machines])
        }
    }

@router.get("/maintenance/statistics")
async def get_maintenance_statistics(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_active_user)
):
    total_tickets = np.random.randint(50, 150)
    
    return {
        "period_days": days,
        "total_tickets": total_tickets,
        "completed_tickets": int(total_tickets * 0.7),
        "pending_tickets": int(total_tickets * 0.3),
        "average_resolution_time_hours": np.random.uniform(4, 12),
        "preventive_maintenance_count": int(total_tickets * 0.6),
        "corrective_maintenance_count": int(total_tickets * 0.4),
        "total_downtime_hours": np.random.uniform(50, 200),
        "total_maintenance_cost": np.random.uniform(50000, 150000),
        "by_priority": {
            "critical": int(total_tickets * 0.1),
            "high": int(total_tickets * 0.2),
            "medium": int(total_tickets * 0.4),
            "low": int(total_tickets * 0.3)
        }
    }

@router.get("/optimization/report")
async def get_optimization_report(
    current_user = Depends(get_current_active_user)
):
    return {
        "timestamp": datetime.utcnow().isoformat(),
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
            },
            {
                "action": "energy_reduction",
                "count": 20,
                "impact": "medium"
            },
            {
                "action": "predictive_maintenance",
                "count": 12,
                "impact": "high"
            }
        ],
        "recommendations": [
            "Continue energy optimization during off-peak hours",
            "Schedule preventive maintenance for machines with health score below 80",
            "Consider equipment upgrade for consistently low-efficiency machines"
        ]
    }