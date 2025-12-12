from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import numpy as np

router = APIRouter(prefix="/maintenance", tags=["maintenance"])

class MaintenanceTicketCreate(BaseModel):
    machine_id: str
    title: str
    description: str
    priority: str
    failure_type: Optional[str]

class MaintenanceTicketResponse(BaseModel):
    id: int
    ticket_id: str
    machine_id: str
    title: str
    description: str
    status: str
    priority: str
    assigned_to: Optional[str]
    reported_by: str
    failure_type: Optional[str]
    estimated_downtime_hours: Optional[float]
    repair_steps: Optional[str]
    parts_required: Optional[str]
    cost_estimate: Optional[float]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

class TicketUpdate(BaseModel):
    status: Optional[str]
    assigned_to: Optional[str]
    repair_steps: Optional[str]
    actual_downtime_hours: Optional[float]
    actual_cost: Optional[float]

@router.post("/tickets", response_model=MaintenanceTicketResponse)
async def create_maintenance_ticket(
    ticket: MaintenanceTicketCreate,
    current_user = Depends(get_current_active_user)
):
    ticket_id = f"MT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    return MaintenanceTicketResponse(
        id=np.random.randint(1, 10000),
        ticket_id=ticket_id,
        machine_id=ticket.machine_id,
        title=ticket.title,
        description=ticket.description,
        status="open",
        priority=ticket.priority,
        assigned_to=None,
        reported_by=current_user.username,
        failure_type=ticket.failure_type,
        estimated_downtime_hours=np.random.uniform(2, 8),
        repair_steps=None,
        parts_required=None,
        cost_estimate=np.random.uniform(500, 5000),
        created_at=datetime.utcnow(),
        started_at=None,
        completed_at=None
    )

@router.get("/tickets", response_model=List[MaintenanceTicketResponse])
async def get_maintenance_tickets(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    machine_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    current_user = Depends(get_current_active_user)
):
    tickets = []
    
    statuses = ["open", "in_progress", "pending_parts", "completed"]
    priorities = ["critical", "high", "medium", "low"]
    
    for i in range(limit):
        ticket_status = np.random.choice(statuses, p=[0.2, 0.3, 0.1, 0.4])
        ticket_priority = np.random.choice(priorities, p=[0.1, 0.2, 0.4, 0.3])
        ticket_machine = f"M{np.random.randint(1, 21):03d}"
        
        if status and ticket_status != status:
            continue
        if priority and ticket_priority != priority:
            continue
        if machine_id and ticket_machine != machine_id:
            continue
        
        created = datetime.utcnow() - timedelta(hours=np.random.randint(1, 168))
        
        ticket = MaintenanceTicketResponse(
            id=i + 1,
            ticket_id=f"MT-{created.strftime('%Y%m%d%H%M%S')}{i:04d}",
            machine_id=ticket_machine,
            title=f"Maintenance required for {ticket_machine}",
            description=f"Issue detected on machine {ticket_machine}",
            status=ticket_status,
            priority=ticket_priority,
            assigned_to=f"technician_{np.random.randint(1, 5)}" if ticket_status != "open" else None,
            reported_by=f"operator_{np.random.randint(1, 5)}",
            failure_type=np.random.choice(["overheating", "mechanical_stress", "pressure_abnormality"]),
            estimated_downtime_hours=np.random.uniform(2, 8),
            repair_steps="Step 1: Inspect components. Step 2: Replace faulty parts. Step 3: Test operation." if ticket_status != "open" else None,
            parts_required="Bearings, Seals" if ticket_status == "pending_parts" else None,
            cost_estimate=np.random.uniform(500, 5000),
            created_at=created,
            started_at=created + timedelta(hours=1) if ticket_status != "open" else None,
            completed_at=created + timedelta(hours=np.random.randint(3, 24)) if ticket_status == "completed" else None
        )
        
        tickets.append(ticket)
    
    return sorted(tickets, key=lambda x: x.created_at, reverse=True)

@router.get("/tickets/{ticket_id}", response_model=MaintenanceTicketResponse)
async def get_maintenance_ticket(
    ticket_id: str,
    current_user = Depends(get_current_active_user)
):
    return MaintenanceTicketResponse(
        id=1,
        ticket_id=ticket_id,
        machine_id="M014",
        title="Bearing overheating issue",
        description="Machine M014 bearings showing signs of overheating",
        status="in_progress",
        priority="high",
        assigned_to="technician_2",
        reported_by="operator_1",
        failure_type="overheating",
        estimated_downtime_hours=6.0,
        repair_steps="Step 1: Shut down machine. Step 2: Cool bearings. Step 3: Inspect lubrication. Step 4: Replace if needed.",
        parts_required="Bearing assembly, Lubricant",
        cost_estimate=2500.0,
        created_at=datetime.utcnow() - timedelta(hours=2),
        started_at=datetime.utcnow() - timedelta(hours=1),
        completed_at=None
    )

@router.patch("/tickets/{ticket_id}")
async def update_maintenance_ticket(
    ticket_id: str,
    update: TicketUpdate,
    current_user = Depends(require_supervisor)
):
    return {
        "ticket_id": ticket_id,
        "updated_fields": update.dict(exclude_unset=True),
        "updated_at": datetime.utcnow().isoformat(),
        "updated_by": current_user.username
    }

@router.post("/tickets/{ticket_id}/assign")
async def assign_ticket(
    ticket_id: str,
    technician: str,
    current_user = Depends(require_supervisor)
):
    return {
        "ticket_id": ticket_id,
        "assigned_to": technician,
        "assigned_by": current_user.username,
        "assigned_at": datetime.utcnow().isoformat(),
        "status": "in_progress"
    }

@router.post("/tickets/{ticket_id}/complete")
async def complete_ticket(
    ticket_id: str,
    completion_notes: str,
    actual_downtime: float,
    actual_cost: float,
    current_user = Depends(get_current_active_user)
):
    return {
        "ticket_id": ticket_id,
        "status": "completed",
        "completed_by": current_user.username,
        "completed_at": datetime.utcnow().isoformat(),
        "completion_notes": completion_notes,
        "actual_downtime_hours": actual_downtime,
        "actual_cost": actual_cost
    }