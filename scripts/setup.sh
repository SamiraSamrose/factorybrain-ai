#!/bin/bash

set -e

echo "FactoryBrain AI - Setup Script"
echo "==============================="
echo ""

echo "Step 1: Creating directories..."
mkdir -p data/raw
mkdir -p ml_models/saved
mkdir -p logs
mkdir -p backend/app/__pycache__
echo "Directories created successfully."

echo ""
echo "Step 2: Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "Virtual environment created and activated."

echo ""
echo "Step 3: Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt
echo "Dependencies installed successfully."

echo ""
echo "Step 4: Copying environment template..."
if [ ! -f deployment/.env ]; then
    cp deployment/.env.template deployment/.env
    echo "Environment file created. Please edit deployment/.env with your API keys."
else
    echo "Environment file already exists."
fi

echo ""
echo "Step 5: Setting up database..."
echo "Make sure PostgreSQL is running on localhost:5432"
read -p "Press enter to continue once PostgreSQL is ready..."

export DATABASE_URL="postgresql://factorybrain:factory_secure_pass@localhost:5432/factorybrain"

echo "Creating database..."
psql -U postgres -c "CREATE DATABASE factorybrain;" 2>/dev/null || echo "Database already exists."
psql -U postgres -c "CREATE USER factorybrain WITH PASSWORD 'factory_secure_pass';" 2>/dev/null || echo "User already exists."
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE factorybrain TO factorybrain;" 2>/dev/null

echo ""
echo "Step 6: Running database migrations..."
cd backend
alembic init alembic 2>/dev/null || echo "Alembic already initialized."
alembic revision --autogenerate -m "Initial migration" 2>/dev/null || echo "Migration already exists."
alembic upgrade head 2>/dev/null || echo "Database already up to date."
cd ..

echo ""
echo "Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit deployment/.env with your API keys"
echo "2. Run ./scripts/data_download.sh to download datasets"
echo "3. Run ./scripts/train_models.sh to train ML models"
echo "4. Run ./scripts/deploy.sh to start the application"
echo ""