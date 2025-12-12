#!/bin/bash

set -e

echo "FactoryBrain AI - Dataset Download Script"
echo "=========================================="
echo ""

DATA_DIR="data/raw"

echo "Downloading datasets to $DATA_DIR..."
echo ""

echo "Note: This script generates synthetic datasets."
echo "For production use, replace with actual industrial sensor data."
echo ""

source venv/bin/activate

echo "Generating sensor faults dataset..."
python3 << EOF
import sys
sys.path.append('.')
from backend.app.data.loaders import DatasetLoader
import asyncio

async def download():
    loader = DatasetLoader()
    await loader.load_sensor_faults_dataset()
    await loader.load_failure_dataset()
    await loader.load_vibration_dataset()
    print("All datasets generated successfully!")

asyncio.run(download())
EOF

echo ""
echo "Dataset generation completed!"
echo ""
echo "Generated datasets:"
echo "- $DATA_DIR/sensor_faults.csv"
echo "- $DATA_DIR/failure_data.csv"
echo "- $DATA_DIR/vibration_data.csv"
echo ""