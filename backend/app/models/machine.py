from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Machine(Base):
    __tablename__ = "machines"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, unique=True, index=True)
    name = Column(String)
    type = Column(String)
    location = Column(String)
    status = Column(String, default="operational")
    health_score = Column(Float, default=100.0)
    temperature = Column(Float)
    vibration = Column(Float)
    pressure = Column(Float)
    power_consumption = Column(Float)
    efficiency = Column(Float)
    uptime_hours = Column(Float, default=0.0)
    last_maintenance = Column(DateTime, default=datetime.utcnow)
    next_maintenance = Column(DateTime)
    failure_probability = Column(Float, default=0.0)
    remaining_useful_life = Column(Float)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SensorReading(Base):
    __tablename__ = "sensor_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, index=True)
    sensor_type = Column(String)
    value = Column(Float)
    unit = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    is_anomaly = Column(Boolean, default=False)
    anomaly_score = Column(Float)