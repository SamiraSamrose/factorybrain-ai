from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import numpy as np

router = APIRouter(prefix="/procurement", tags=["procurement"])

class ProcurementOrderCreate(BaseModel):
    part_name: str
    part_number: str
    quantity: int
    urgency: str
    machine_id: Optional[str]
    ticket_id: Optional[str]

class ProcurementOrderResponse(BaseModel):
    id: int
    order_id: str
    part_name: str
    part_number: str
    quantity: int
    supplier: str
    unit_price: float
    total_price: float
    negotiated_price: float
    savings: float
    status: str
    urgency: str
    machine_id: Optional[str]
    ticket_id: Optional[str]
    requested_by: str
    approved_by: Optional[str]
    estimated_delivery: datetime
    created_at: datetime

class InventoryItem(BaseModel):
    id: int
    part_name: str
    part_number: str
    quantity: int
    reorder_level: int
    location: str
    cost_per_unit: float
    last_restocked: Optional[datetime]

@router.post("/orders", response_model=ProcurementOrderResponse)
async def create_procurement_order(
    order: ProcurementOrderCreate,
    current_user = Depends(get_current_active_user)
):
    order_id = f"PO-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    unit_price = np.random.uniform(50, 500)
    negotiated_price = unit_price * 0.88
    
    return ProcurementOrderResponse(
        id=np.random.randint(1, 10000),
        order_id=order_id,
        part_name=order.part_name,
        part_number=order.part_number,
        quantity=order.quantity,
        supplier="Industrial Parts Co",
        unit_price=unit_price,
        total_price=unit_price * order.quantity,
        negotiated_price=negotiated_price,
        savings=(unit_price - negotiated_price) * order.quantity,
        status="requested",
        urgency=order.urgency,
        machine_id=order.machine_id,
        ticket_id=order.ticket_id,
        requested_by=current_user.username,
        approved_by=None,
        estimated_delivery=datetime.utcnow() + timedelta(days=np.random.randint(2, 7)),
        created_at=datetime.utcnow()
    )

@router.get("/orders", response_model=List[ProcurementOrderResponse])
async def get_procurement_orders(
    status: Optional[str] = Query(None),
    urgency: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    current_user = Depends(get_current_active_user)
):
    orders = []
    
    statuses = ["requested", "negotiating", "ordered", "shipped", "delivered"]
    urgencies = ["critical", "high", "medium", "low"]
    
    for i in range(limit):
        order_status = np.random.choice(statuses, p=[0.2, 0.15, 0.3, 0.2, 0.15])
        order_urgency = np.random.choice(urgencies, p=[0.1, 0.2, 0.4, 0.3])
        
        if status and order_status != status:
            continue
        if urgency and order_urgency != urgency:
            continue
        
        unit_price = np.random.uniform(50, 500)
        quantity = np.random.randint(1, 20)
        negotiated_price = unit_price * np.random.uniform(0.85, 0.95)
        created = datetime.utcnow() - timedelta(days=np.random.randint(0, 30))
        
        order = ProcurementOrderResponse(
            id=i + 1,
            order_id=f"PO-{created.strftime('%Y%m%d%H%M%S')}{i:04d}",
            part_name=f"Part {np.random.randint(100, 999)}",
            part_number=f"PN-{np.random.randint(10000, 99999)}",
            quantity=quantity,
            supplier=np.random.choice(["Industrial Parts Co", "MachineSupply Direct", "Precision Components Ltd"]),
            unit_price=unit_price,
            total_price=unit_price * quantity,
            negotiated_price=negotiated_price,
            savings=(unit_price - negotiated_price) * quantity,
            status=order_status,
            urgency=order_urgency,
            machine_id=f"M{np.random.randint(1, 21):03d}",
            ticket_id=f"MT-{np.random.randint(1000, 9999)}",
            requested_by=f"operator_{np.random.randint(1, 5)}",
            approved_by=f"supervisor_{np.random.randint(1, 3)}" if order_status != "requested" else None,
            estimated_delivery=created + timedelta(days=np.random.randint(2, 7)),
            created_at=created
        )
        
        orders.append(order)
    
    return sorted(orders, key=lambda x: x.created_at, reverse=True)

@router.get("/orders/{order_id}", response_model=ProcurementOrderResponse)
async def get_procurement_order(
    order_id: str,
    current_user = Depends(get_current_active_user)
):
    return ProcurementOrderResponse(
        id=1,
        order_id=order_id,
        part_name="Bearing Assembly",
        part_number="PN-45678",
        quantity=5,
        supplier="Industrial Parts Co",
        unit_price=250.0,
        total_price=1250.0,
        negotiated_price=220.0,
        savings=150.0,
        status="ordered",
        urgency="high",
        machine_id="M014",
        ticket_id="MT-20241207001",
        requested_by="operator_1",
        approved_by="supervisor_1",
        estimated_delivery=datetime.utcnow() + timedelta(days=3),
        created_at=datetime.utcnow() - timedelta(hours=6)
    )

@router.post("/orders/{order_id}/approve")
async def approve_procurement_order(
    order_id: str,
    current_user = Depends(require_supervisor)
):
    return {
        "order_id": order_id,
        "status": "ordered",
        "approved_by": current_user.username,
        "approved_at": datetime.utcnow().isoformat()
    }

@router.get("/inventory", response_model=List[InventoryItem])
async def get_inventory(
    low_stock_only: bool = Query(False),
    current_user = Depends(get_current_active_user)
):
    inventory = []
    
    for i in range(50):
        quantity = np.random.randint(0, 50)
        reorder_level = 10
        
        if low_stock_only and quantity > reorder_level:
            continue
        
        inventory.append(InventoryItem(
            id=i + 1,
            part_name=f"Part {np.random.randint(100, 999)}",
            part_number=f"PN-{np.random.randint(10000, 99999)}",
            quantity=quantity,
            reorder_level=reorder_level,
            location=f"Warehouse {np.random.choice(['A', 'B', 'C'])}-{np.random.randint(1, 20)}",
            cost_per_unit=np.random.uniform(50, 500),
            last_restocked=datetime.utcnow() - timedelta(days=np.random.randint(1, 90)) if quantity > 0 else None
        ))
    
    return inventory

@router.get("/inventory/{part_number}", response_model=InventoryItem)
async def get_inventory_item(
    part_number: str,
    current_user = Depends(get_current_active_user)
):
    return InventoryItem(
        id=1,
        part_name="Bearing Assembly",
        part_number=part_number,
        quantity=8,
        reorder_level=10,
        location="Warehouse A-5",
        cost_per_unit=250.0,
        last_restocked=datetime.utcnow() - timedelta(days=15)
    )

@router.get("/statistics/summary")
async def get_procurement_statistics(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_active_user)
):
    total_orders = np.random.randint(50, 200)
    
    return {
        "period_days": days,
        "total_orders": total_orders,
        "total_spent": np.random.uniform(50000, 200000),
        "total_savings": np.random.uniform(5000, 20000),
        "average_delivery_time_days": np.random.uniform(3, 7),
        "pending_orders": int(total_orders * 0.3),
        "completed_orders": int(total_orders * 0.7),
        "low_stock_items": np.random.randint(5, 20),
        "top_suppliers": [
            {"name": "Industrial Parts Co", "orders": int(total_orders * 0.4), "total_value": np.random.uniform(20000, 80000)},
            {"name": "MachineSupply Direct", "orders": int(total_orders * 0.3), "total_value": np.random.uniform(15000, 60000)},
            {"name": "Precision Components Ltd", "orders": int(total_orders * 0.3), "total_value": np.random.uniform(15000, 60000)}
        ]
    }