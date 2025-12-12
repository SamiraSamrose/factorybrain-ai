import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import asyncio
from backend.app.data.loaders import DatasetLoader
from backend.app.services.ml_service import MLService

async def train_anomaly_detector():
    print("Starting anomaly detection model training...")
    
    loader = DatasetLoader()
    ml_service = MLService()
    
    print("Loading sensor faults dataset...")
    sensor_data = await loader.load_sensor_faults_dataset()
    
    print(f"Dataset loaded: {len(sensor_data)} samples")
    print(f"Anomaly distribution: {sensor_data['is_anomaly'].value_counts().to_dict()}")
    
    print("\nTraining anomaly detection model...")
    results = await ml_service.train_anomaly_detector(sensor_data)
    
    print("\nTraining Results:")
    print(f"Model: {results['model_name']}")
    print(f"Training Accuracy: {results['train_accuracy']:.4f}")
    print(f"Test Accuracy: {results['test_accuracy']:.4f}")
    print(f"Training Samples: {results['training_samples']}")
    print(f"Test Samples: {results['test_samples']}")
    
    print("\nFeature Importance:")
    for feature, importance in results['feature_importance'].items():
        print(f"  {feature}: {importance:.4f}")
    
    print(f"\nModel saved successfully at: ml_models/saved/anomaly_detector.pkl")

if __name__ == "__main__":
    asyncio.run(train_anomaly_detector())