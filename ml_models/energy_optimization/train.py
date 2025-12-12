import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import asyncio
from backend.app.data.loaders import DatasetLoader
from backend.app.services.ml_service import MLService

async def train_rul_estimator():
    print("Starting RUL estimation model training...")
    
    loader = DatasetLoader()
    ml_service = MLService()
    
    print("Loading failure dataset...")
    failure_data = await loader.load_failure_dataset()
    
    print(f"Dataset loaded: {len(failure_data)} samples")
    
    print("\nTraining RUL estimation model...")
    results = await ml_service.train_rul_estimator(failure_data)
    
    print("\nTraining Results:")
    print(f"Model: {results['model_name']}")
    print(f"Training R2 Score: {results['train_r2_score']:.4f}")
    print(f"Test R2 Score: {results['test_r2_score']:.4f}")
    print(f"MAE: {results['mae']:.4f}")
    print(f"RMSE: {results['rmse']:.4f}")
    print(f"Training Samples: {results['training_samples']}")
    print(f"Test Samples: {results['test_samples']}")
    
    print(f"\nModel saved successfully at: ml_models/saved/rul_estimator.pkl")

if __name__ == "__main__":
    asyncio.run(train_rul_estimator())