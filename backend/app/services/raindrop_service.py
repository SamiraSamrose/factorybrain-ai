import httpx
from typing import Dict, Any, List
import json

class RaindropService:
    def __init__(self, config):
        self.bucket_endpoint = config.RAINDROP_BUCKET_ENDPOINT
        self.sql_endpoint = config.RAINDROP_SQL_ENDPOINT
        self.memory_endpoint = config.RAINDROP_MEMORY_ENDPOINT
        self.inference_endpoint = config.RAINDROP_INFERENCE_ENDPOINT
        
    async def store_sensor_data(self, machine_id: str, sensor_data: Dict[str, Any]) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.bucket_endpoint}/smartbuckets/sensor_data",
                    json={
                        "machine_id": machine_id,
                        "data": sensor_data,
                        "timestamp": sensor_data.get("timestamp")
                    }
                )
                return response.status_code == 200
            except Exception as e:
                print(f"Error storing sensor data: {e}")
                return False
    
    async def query_operational_analytics(self, query: str) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.sql_endpoint}/smartsql/query",
                    json={"query": query}
                )
                return response.json().get("results", [])
            except Exception as e:
                print(f"Error querying analytics: {e}")
                return []
    
    async def store_machine_memory(self, machine_id: str, memory_data: Dict[str, Any]) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.memory_endpoint}/smartmemory/store",
                    json={
                        "machine_id": machine_id,
                        "memory": memory_data
                    }
                )
                return response.status_code == 200
            except Exception as e:
                print(f"Error storing machine memory: {e}")
                return False
    
    async def retrieve_machine_memory(self, machine_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.memory_endpoint}/smartmemory/retrieve/{machine_id}"
                )
                return response.json().get("memory", {})
            except Exception as e:
                print(f"Error retrieving machine memory: {e}")
                return {}
    
    async def route_ml_inference(self, model_name: str, input_data: Any) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.inference_endpoint}/smartinference/predict",
                    json={
                        "model": model_name,
                        "input": input_data
                    }
                )
                return response.json()
            except Exception as e:
                print(f"Error routing ML inference: {e}")
                return {"error": str(e)}
    
    async def store_kpis(self, kpis: Dict[str, float]) -> bool:
        return await self.store_sensor_data("plant_kpis", kpis)
    
    async def store_energy_metrics(self, metrics: Dict[str, Any]) -> bool:
        return await self.store_sensor_data("energy_metrics", metrics)
    
    async def get_machine_history(self, machine_id: str, days: int = 7) -> List[Dict[str, Any]]:
        query = f"""
        SELECT * FROM sensor_readings 
        WHERE machine_id = '{machine_id}' 
        AND timestamp >= NOW() - INTERVAL '{days} days'
        ORDER BY timestamp DESC
        """
        return await self.query_operational_analytics(query)
