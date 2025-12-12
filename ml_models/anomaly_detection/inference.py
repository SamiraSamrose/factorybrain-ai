import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import asyncio
from backend.app.services.ml_service import MLService

async def run_inference():
    ml_service = MLService()
    
    test_sensor_data = {
        'temperature': 92.5,
        'vibration': 0.85,
        'pressure': 58.0,
        'power_consumption': 75.0
    }
    
    print("Running anomaly detection inference...")
    print(f"Input sensor data: {test_sensor_data}")
    
    result = await ml_service.predict_anomaly(test_sensor_data)
    
    print("\nInference Results:")
    print(f"Is Anomaly: {result['is_anomaly']}")
    print(f"Anomaly Score: {result['anomaly_score']:.4f}")
    print(f"Confidence: {result['confidence']:.4f}")
    print(f"Timestamp: {result['timestamp']}")

if __name__ == "__main__":
    asyncio.run(run_inference())