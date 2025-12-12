import httpx
from typing import Dict, Any
import asyncio

class CerebrasService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.cerebras.ai/v1"
        self.inference_count = 0
        self.avg_latency_ms = 0
        
    async def inference_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        start_time = asyncio.get_event_loop().time()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        endpoint = f"{self.base_url}/inference"
        
        async with httpx.AsyncClient(timeout=2.0) as client:
            try:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers
                )
                
                end_time = asyncio.get_event_loop().time()
                latency_ms = (end_time - start_time) * 1000
                
                self.inference_count += 1
                self.avg_latency_ms = (
                    (self.avg_latency_ms * (self.inference_count - 1) + latency_ms) / 
                    self.inference_count
                )
                
                result = response.json()
                result["latency_ms"] = latency_ms
                
                return result
                
            except httpx.TimeoutException:
                return {
                    "error": "Request timeout",
                    "latency_ms": 2000,
                    "fallback": True
                }
            except Exception as e:
                return {
                    "error": str(e),
                    "fallback": True
                }
    
    async def anomaly_detection_inference(self, sensor_features: list) -> Dict[str, Any]:
        payload = {
            "model": "anomaly_detector_v1",
            "inputs": sensor_features,
            "ultra_low_latency": True,
            "max_latency_ms": 50
        }
        
        response = await self.inference_request(payload)
        
        if response.get("fallback"):
            return {
                "anomaly_score": 0.0,
                "is_anomaly": False,
                "confidence": 0.0,
                "latency_ms": response.get("latency_ms", 0)
            }
        
        return {
            "anomaly_score": response.get("predictions", [0.0])[0],
            "is_anomaly": response.get("predictions", [0.0])[0] > 0.75,
            "confidence": response.get("confidence", 0.0),
            "latency_ms": response.get("latency_ms", 0)
        }
    
    async def failure_prediction_inference(self, historical_features: list) -> Dict[str, Any]:
        payload = {
            "model": "failure_predictor_v1",
            "inputs": historical_features,
            "ultra_low_latency": True,
            "return_probabilities": True
        }
        
        response = await self.inference_request(payload)
        
        if response.get("fallback"):
            return {
                "failure_probability": 0.0,
                "estimated_hours": None,
                "confidence": 0.0
            }
        
        predictions = response.get("predictions", [0.0])
        
        return {
            "failure_probability": predictions[0],
            "estimated_hours": predictions[1] if len(predictions) > 1 else None,
            "confidence": response.get("confidence", 0.0),
            "latency_ms": response.get("latency_ms", 0)
        }
    
    async def control_loop_decision(self, machine_state: Dict[str, float]) -> Dict[str, Any]:
        payload = {
            "model": "control_optimizer_v1",
            "inputs": list(machine_state.values()),
            "ultra_low_latency": True,
            "max_latency_ms": 10
        }
        
        response = await self.inference_request(payload)
        
        return {
            "recommended_action": response.get("action", "maintain"),
            "confidence": response.get("confidence", 0.0),
            "parameters": response.get("parameters", {}),
            "latency_ms": response.get("latency_ms", 0)
        }
    
    async def get_inference_stats(self) -> Dict[str, Any]:
        return {
            "total_inferences": self.inference_count,
            "average_latency_ms": self.avg_latency_ms,
            "ultra_low_latency_enabled": True,
            "target_latency_ms": 50
        }
