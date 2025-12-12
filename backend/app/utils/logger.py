import logging
import json
from datetime import datetime
from typing import Dict, Any
import os

class FactoryBrainLogger:
    def __init__(self, name: str, log_dir: str = "logs"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(
            os.path.join(log_dir, f'{name}_{datetime.utcnow().strftime("%Y%m%d")}.log')
            )

        file_handler.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    self.logger.addHandler(file_handler)
    self.logger.addHandler(console_handler)

def log_event(self, event_type: str, data: Dict[str, Any], level: str = "info"):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "data": data
    }
    
    log_message = json.dumps(log_entry)
    
    if level == "info":
        self.logger.info(log_message)
    elif level == "warning":
        self.logger.warning(log_message)
    elif level == "error":
        self.logger.error(log_message)
    elif level == "critical":
        self.logger.critical(log_message)

def log_machine_event(self, machine_id: str, event: str, details: Dict[str, Any]):
    self.log_event("machine_event", {
        "machine_id": machine_id,
        "event": event,
        "details": details
    })

def log_agent_action(self, agent_name: str, action: str, result: Dict[str, Any]):
    self.log_event("agent_action", {
        "agent": agent_name,
        "action": action,
        "result": result
    })

def log_api_request(self, endpoint: str, method: str, user: str, status_code: int):
    self.log_event("api_request", {
        "endpoint": endpoint,
        "method": method,
        "user": user,
        "status_code": status_code
    })

def log_error(self, error_type: str, error_message: str, stack_trace: str = None):
    self.log_event("error", {
        "error_type": error_type,
        "message": error_message,
        "stack_trace": stack_trace
    }, level="error")