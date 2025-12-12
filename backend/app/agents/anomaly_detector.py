import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
import asyncio

class AnomalyDetectorAgent:
    def __init__(self, cerebras_service, db_session):
        self.cerebras = cerebras_service
        self.db = db_session
        self.models = {}
        self.anomaly_history = []
        self.detection_threshold = 0.75
        
    async def detect_sensor_anomalies(self, machine_id: str, sensor_data: Dict[str, float]) -> Dict[str, Any]:
        features = np.array([
            sensor_data.get("temperature", 0),
            sensor_data.get("vibration", 0),
            sensor_data.get("pressure", 0),
            sensor_data.get("power_consumption", 0)
        ]).reshape(1, -1)
        
        cerebras_response = await self.cerebras.inference_request({
            "model": "anomaly_detection",
            "input_features": features.tolist(),
            "machine_id": machine_id
        })
        
        anomaly_score = cerebras_response.get("anomaly_score", 0.0)
        is_anomaly = anomaly_score > self.detection_threshold
        
        anomaly_result = {
            "machine_id": machine_id,
            "timestamp": datetime.utcnow().isoformat(),
            "anomaly_score": anomaly_score,
            "is_anomaly": is_anomaly,
            "sensor_data": sensor_data,
            "anomaly_type": self._classify_anomaly_type(sensor_data, anomaly_score) if is_anomaly else None
        }
        
        if is_anomaly:
            self.anomaly_history.append(anomaly_result)
            await self._trigger_alert(anomaly_result)
        
        return anomaly_result
    
    def _classify_anomaly_type(self, sensor_data: Dict[str, float], score: float) -> str:
        if sensor_data.get("temperature", 0) > 85:
            return "overheating"
        elif sensor_data.get("vibration", 0) > 0.8:
            return "mechanical_stress"
        elif sensor_data.get("pressure", 0) < 20 or sensor_data.get("pressure", 0) > 100:
            return "pressure_abnormality"
        elif sensor_data.get("power_consumption", 0) > 80:
            return "power_surge"
        else:
            return "general_anomaly"
    
    async def predict_failure(self, machine_id: str, historical_data: List[Dict]) -> Dict[str, Any]:
        if len(historical_data) < 10:
            return {"failure_probability": 0.0, "confidence": "low"}
        
        features = self._extract_failure_features(historical_data)
        
        cerebras_response = await self.cerebras.inference_request({
            "model": "failure_prediction",
            "input_features": features.tolist(),
            "machine_id": machine_id,
            "ultra_low_latency": True
        })
        
        failure_prob = cerebras_response.get("failure_probability", 0.0)
        time_to_failure = cerebras_response.get("estimated_hours", None)
        
        prediction = {
            "machine_id": machine_id,
            "timestamp": datetime.utcnow().isoformat(),
            "failure_probability": failure_prob,
            "estimated_time_to_failure_hours": time_to_failure,
            "confidence": "high" if len(historical_data) > 50 else "medium",
            "contributing_factors": self._identify_failure_factors(historical_data)
        }
        
        if failure_prob > 0.7:
            await self._trigger_failure_alert(prediction)
        
        return prediction
    
    def _extract_failure_features(self, historical_data: List[Dict]) -> np.ndarray:
        temps = [d.get("temperature", 0) for d in historical_data[-20:]]
        vibes = [d.get("vibration", 0) for d in historical_data[-20:]]
        
        features = [
            np.mean(temps),
            np.std(temps),
            np.max(temps),
            np.mean(vibes),
            np.std(vibes),
            np.max(vibes),
            len([t for t in temps if t > 80]),
            len([v for v in vibes if v > 0.7])
        ]
        
        return np.array(features).reshape(1, -1)
    
    def _identify_failure_factors(self, historical_data: List[Dict]) -> List[str]:
        factors = []
        recent = historical_data[-10:]
        
        if np.mean([d.get("temperature", 0) for d in recent]) > 80:
            factors.append("sustained_high_temperature")
        
        if np.mean([d.get("vibration", 0) for d in recent]) > 0.7:
            factors.append("excessive_vibration")
        
        if len([d for d in recent if d.get("power_consumption", 0) > 75]) > 5:
            factors.append("power_instability")
        
        return factors
    
    async def _trigger_alert(self, anomaly_result: Dict):
        alert = {
            "type": "anomaly_detected",
            "machine_id": anomaly_result["machine_id"],
            "severity": "high" if anomaly_result["anomaly_score"] > 0.85 else "medium",
            "message": f"Anomaly detected: {anomaly_result.get('anomaly_type', 'unknown')}",
            "timestamp": anomaly_result["timestamp"]
        }
        await self.db.create_alert(alert)
    
    async def _trigger_failure_alert(self, prediction: Dict):
        alert = {
            "type": "failure_prediction",
            "machine_id": prediction["machine_id"],
            "severity": "critical",
            "message": f"Failure probability: {prediction['failure_probability']:.2%}",
            "estimated_time": prediction.get("estimated_time_to_failure_hours"),
            "timestamp": prediction["timestamp"]
        }
        await self.db.create_alert(alert)
    
    async def analyze_vibration_patterns(self, machine_id: str, audio_data: bytes) -> Dict[str, Any]:
        cerebras_response = await self.cerebras.inference_request({
            "model": "vibration_analysis",
            "audio_data": audio_data,
            "machine_id": machine_id,
            "ultra_low_latency": True
        })
        
        return {
            "machine_id": machine_id,
            "timestamp": datetime.utcnow().isoformat(),
            "bearing_condition": cerebras_response.get("bearing_health", "unknown"),
            "vibration_frequency": cerebras_response.get("dominant_frequency", 0),
            "anomaly_detected": cerebras_response.get("is_anomalous", False)
        }