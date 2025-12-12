from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import numpy as np

router = APIRouter(prefix="/alerts", tags=["alerts"])

class AlertResponse(BaseModel):
    id: int
    alert_type: str
    machine_id: str
    severity: str
    message: str
    timestamp: datetime
    acknowledged: bool
    acknowledged_by: Optional[str]
    resolved: bool

class AlertAcknowledge(BaseModel):
    acknowledged_by: str
    notes: Optional[str]

@router.get("/", response_model=List[AlertResponse])
async def get_all_alerts(
    severity: Optional[str] = Query(None),
    machine_id: Optional[str] = Query(None),
    resolved: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    current_user = Depends(get_current_active_user)
):
    alerts = []
    
    alert_types = ["anomaly_detected", "failure_prediction", "overheating", "vibration_alert", "pressure_abnormal"]
    severities = ["critical", "high", "medium", "low"]
    
    for i in range(limit):
        alert_severity = np.random.choice(severities, p=[0.1, 0.2, 0.4, 0.3])
        alert_machine = f"M{np.random.randint(1, 21):03d}"
        
        if severity and alert_severity != severity:
            continue
        if machine_id and alert_machine != machine_id:
            continue
        
        is_resolved = np.random.random() > 0.6
        if resolved is not None and is_resolved != resolved:
            continue
        
        alert = AlertResponse(
            id=i + 1,
            alert_type=np.random.choice(alert_types),
            machine_id=alert_machine,
            severity=alert_severity,
            message=f"Alert detected on {alert_machine}",
            timestamp=datetime.utcnow() - timedelta(hours=np.random.randint(0, 48)),
            acknowledged=np.random.random() > 0.4,
            acknowledged_by=f"operator_{np.random.randint(1, 5)}" if np.random.random() > 0.4 else None,
            resolved=is_resolved
        )
        
        alerts.append(alert)
    
    return sorted(alerts, key=lambda x: x.timestamp, reverse=True)

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: int,
    current_user = Depends(get_current_active_user)
):
    return AlertResponse(
        id=alert_id,
        alert_type="overheating",
        machine_id="M014",
        severity="critical",
        message="Machine M014 bearings overheating. Current temperature: 95 degrees Celsius",
        timestamp=datetime.utcnow(),
        acknowledged=False,
        acknowledged_by=None,
        resolved=False
    )

@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: int,
    acknowledge_data: AlertAcknowledge,
    current_user = Depends(get_current_active_user)
):
    return {
        "alert_id": alert_id,
        "acknowledged": True,
        "acknowledged_by": acknowledge_data.acknowledged_by,
        "acknowledged_at": datetime.utcnow().isoformat(),
        "notes": acknowledge_data.notes
    }

@router.post("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    resolution_notes: str,
    current_user = Depends(require_supervisor)
):
    return {
        "alert_id": alert_id,
        "resolved": True,
        "resolved_by": current_user.username,
        "resolved_at": datetime.utcnow().isoformat(),
        "resolution_notes": resolution_notes
    }

@router.get("/statistics/summary")
async def get_alert_statistics(
    hours: int = Query(24, ge=1, le=168),
    current_user = Depends(get_current_active_user)
):
    total_alerts = np.random.randint(50, 200)
    
    return {
        "period_hours": hours,
        "total_alerts": total_alerts,
        "by_severity": {
            "critical": int(total_alerts * 0.1),
            "high": int(total_alerts * 0.2),
            "medium": int(total_alerts * 0.4),
            "low": int(total_alerts * 0.3)
        },
        "by_type": {
            "anomaly_detected": int(total_alerts * 0.3),
            "failure_prediction": int(total_alerts * 0.2),
            "overheating": int(total_alerts * 0.2),
            "vibration_alert": int(total_alerts * 0.15),
            "pressure_abnormal": int(total_alerts * 0.15)
        },
        "acknowledged_count": int(total_alerts * 0.7),
        "resolved_count": int(total_alerts * 0.5),
        "average_response_time_minutes": np.random.uniform(15, 45)
    }