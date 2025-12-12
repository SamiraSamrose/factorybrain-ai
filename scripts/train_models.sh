#!/bin/bash

set -e

echo "FactoryBrain AI - Model Training Script"
echo "========================================"
echo ""

source venv/bin/activate

echo "Training anomaly detection model..."
python3 ml_models/anomaly_detection/train.py

echo ""
echo "Training failure prediction model..."
python3 ml_models/predictive_maintenance/train.py

echo ""
echo "Training RUL estimation model..."
python3 ml_models/energy_optimization/train.py

echo ""
echo "All models trained successfully!"
echo ""
echo "Model files saved in: ml_models/saved/"
echo ""