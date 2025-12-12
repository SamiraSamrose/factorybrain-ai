import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import asyncio
from backend.app.data.loaders import DatasetLoader
from backend.app.services.ml_service import MLService

async def train_failure_predictor():
    print("Starting failure prediction model training...")
    
    loader = DatasetLoader()
    ml_service = MLService()
    
    print("Loading failure dataset...")
    failure_data = await loader.load_failure_dataset()
    
    print(f"Dataset loaded: {len(failure_data)} samples")
    print(f"Unique machines: {failure_data['machine_id'].nunique()}")
    
    print("\nTraining failure prediction model...")
    results = await ml_service.train_failure_predictor(failure_data)
    
    print("\nTraining Results:")
    print(f"Model: {results['model_name']}")
    print(f"Training R2 Score: {results['train_r2_score']:.4f}")
    print(f"Test R2 Score: {results['test_r2_score']:.4f}")
    print(f"Training Samples: {results['training_samples']}")
    print(f"Test Samples: {results['test_samples']}")
    
    print("\nFeature Importance:")
    for feature, importance in results['feature_importance'].items():
        print(f"  {feature}: {importance:.4f}")
    
    print(f"\nModel saved successfully at: ml_models/saved/failure_predictor.pkl")

if __name__ == "__main__":
    asyncio.run(train_failure_predictor())