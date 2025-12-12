import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import asyncio
from backend.app.services.ml_service import MLService

async def run_inference():
    ml_service = MLService()
    
    test_machine_data = {
        'cycle': 150,
        'temperature': 85.0,
        'vibration': 0.75,
        'pressure': 62.0,
        'power_consumption': 55.0
    }
    
    print("Running RUL estimation inference...")
    print(f"Input machine data: {test_machine_data}")
    
    result = await ml_service.estimate_rul(test_machine_data)
    
    print("\nInference Results:")
    print(f"Remaining Useful Life: {result['remaining_useful_life_hours']:.2f} hours")
    print(f"Estimated Days: {result['estimated_days']:.2f} days")
    print(f"Maintenance Recommended: {result['maintenance_recommended']}")
    print(f"Timestamp: {result['timestamp']}")

if __name__ == "__main__":
    asyncio.run(run_inference())