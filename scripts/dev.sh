#!/bin/bash
# Development startup script

set -e

echo "Starting CyberMentorTok development environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Start infrastructure
echo "Starting infrastructure services..."
cd infrastructure/docker
docker-compose up -d postgres redis rabbitmq minio opensearch clickhouse

echo "Waiting for services to be ready..."
sleep 10

# Start backend
echo "Starting backend server..."
cd ../../backend
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Seed knowledge graph
echo "Seeding knowledge graph..."
python -m scripts.seed_db

# Start API server
echo "Starting FastAPI server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# Start Celery worker
echo "Starting Celery worker..."
celery -A app.workers.celery_app worker --loglevel=info &

echo "Backend started at http://localhost:8000"
echo "API docs at http://localhost:8000/docs"

# Start frontend
echo "Starting Flutter frontend..."
cd ../frontend
flutter run -d chrome

wait
