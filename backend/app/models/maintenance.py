from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING_PARTS = "pending_parts"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MaintenanceTicket(Base):
    __tablename__ = "maintenance_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)
    machine_id = Column(String, index=True)
    title = Column(String)
    description = Column(Text)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM)
    assigned_to = Column(String)
    reported_by = Column(String)
    failure_type = Column(String)
    estimated_downtime_hours = Column(Float)
    actual_downtime_hours = Column(Float)
    repair_steps = Column(Text)
    parts_required = Column(Text)
    cost_estimate = Column(Float)
    actual_cost = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)