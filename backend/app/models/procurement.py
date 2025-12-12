from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ProcurementStatus(str, enum.Enum):
    REQUESTED = "requested"
    NEGOTIATING = "negotiating"
    ORDERED = "ordered"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class ProcurementOrder(Base):
    __tablename__ = "procurement_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    part_name = Column(String)
    part_number = Column(String)
    quantity = Column(Integer)
    supplier = Column(String)
    unit_price = Column(Float)
    total_price = Column(Float)
    negotiated_price = Column(Float)
    savings = Column(Float)
    status = Column(Enum(ProcurementStatus), default=ProcurementStatus.REQUESTED)
    urgency = Column(String)
    machine_id = Column(String)
    ticket_id = Column(String)
    requested_by = Column(String)
    approved_by = Column(String)
    estimated_delivery = Column(DateTime)
    actual_delivery = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    part_name = Column(String)
    part_number = Column(String, unique=True, index=True)
    quantity = Column(Integer, default=0)
    reorder_level = Column(Integer, default=5)
    location = Column(String)
    cost_per_unit = Column(Float)
    last_restocked = Column(DateTime)