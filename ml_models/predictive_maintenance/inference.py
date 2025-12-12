import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import asyncio
from backend.app.services.ml_service import MLService

async def run_inference():
    ml_service = MLService()
    
    test_features = {
        'temperature_mean': 85.0,
        'temperature_std': 5.2,
        'temperature_max': 95.0,
        'vibration_mean': 0.72,
        'vibration_std': 0.08,
        'vibration_max': 0.85,
        'high_temp_count': 7,
        'high_vibe_count': 5
    }
    
    print("Running failure prediction inference...")
    print(f"Input features: {test_features}")
    
    result = await ml_service.predict_failure(test_features)
    
    print("\nInference Results:")
    print(f"Failure Probability: {result['failure_probability']:.4f}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Timestamp: {result['timestamp']}")

if __name__ == "__main__":
    asyncio.run(run_inference())