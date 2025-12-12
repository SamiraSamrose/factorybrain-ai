import asyncio
import json
from typing import Dict, Any, Callable
from datetime import datetime
import paho.mqtt.client as mqtt

class IoTBrokerService:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client = mqtt.Client()
        self.subscribers = {}
        self.message_count = 0
        self.connected = False
        
    async def connect(self):
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        
        try:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()
            self.connected = True
        except Exception as e:
            print(f"Failed to connect to IoT broker: {e}")
            self.connected = False
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to IoT broker")
            self.client.subscribe("factory/machines/+/sensors")
            self.client.subscribe("factory/alerts/#")
        else:
            print(f"Connection failed with code {rc}")
    
    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            topic_parts = msg.topic.split('/')
            
            if len(topic_parts) >= 4 and topic_parts[2] != '+':
                machine_id = topic_parts[2]
                
                for callback in self.subscribers.get(machine_id, []):
                    asyncio.create_task(callback(machine_id, payload))
                
                for callback in self.subscribers.get('all', []):
                    asyncio.create_task(callback(machine_id, payload))
            
            self.message_count += 1
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        if rc != 0:
            print(f"Unexpected disconnection. Code: {rc}")
    
    async def subscribe_to_machine(self, machine_id: str, callback: Callable):
        if machine_id not in self.subscribers:
            self.subscribers[machine_id] = []
        self.subscribers[machine_id].append(callback)
    
    async def subscribe_to_all_machines(self, callback: Callable):
        if 'all' not in self.subscribers:
            self.subscribers['all'] = []
        self.subscribers['all'].append(callback)
    
    async def publish_sensor_data(self, machine_id: str, sensor_data: Dict[str, Any]):
        topic = f"factory/machines/{machine_id}/sensors"
        payload = json.dumps({
            **sensor_data,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        self.client.publish(topic, payload, qos=1)
    
    async def publish_alert(self, alert_type: str, alert_data: Dict[str, Any]):
        topic = f"factory/alerts/{alert_type}"
        payload = json.dumps({
            **alert_data,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        self.client.publish(topic, payload, qos=2)
    
    async def get_broker_stats(self) -> Dict[str, Any]:
        return {
            "connected": self.connected,
            "host": self.host,
            "port": self.port,
            "total_messages": self.message_count,
            "active_subscriptions": sum(len(subs) for subs in self.subscribers.values()),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.connected = False