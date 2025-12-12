#!/bin/bash

set -e

echo "FactoryBrain AI - Deployment Script"
echo "===================================="
echo ""

read -p "Select deployment method (1=Docker Compose, 2=Kubernetes): " DEPLOY_METHOD

if [ "$DEPLOY_METHOD" = "1" ]; then
    echo ""
    echo "Deploying with Docker Compose..."
    echo ""
    
    cd deployment
    
    if [ ! -f .env ]; then
        echo "Error: .env file not found. Please copy .env.template to .env and configure it."
        exit 1
    fi
    
    docker-compose down
    docker-compose build
    docker-compose up -d
    
    echo ""
    echo "Waiting for services to start..."
    sleep 10
    
    echo ""
    echo "Deployment completed!"
    echo ""
    echo "Services:"
    echo "- Frontend: http://localhost"
    echo "- Backend API: http://localhost:8000"
    echo "- API Docs: http://localhost:8000/docs"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
    echo ""

elif [ "$DEPLOY_METHOD" = "2" ]; then
    echo ""
    echo "Deploying to Kubernetes..."
    echo ""
    
    kubectl apply -f deployment/kubernetes/namespace.yaml
    kubectl apply -f deployment/kubernetes/backend-deployment.yaml
    kubectl apply -f deployment/kubernetes/frontend-deployment.yaml
    kubectl apply -f deployment/kubernetes/ml-worker-deployment.yaml
    kubectl apply -f deployment/kubernetes/services.yaml
    kubectl apply -f deployment/kubernetes/ingress.yaml
    
    echo ""
    echo "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod -l app=factorybrain-backend -n factorybrain --timeout=300s
    kubectl wait --for=condition=ready pod -l app=factorybrain-frontend -n factorybrain --timeout=300s
    
    echo ""
    echo "Deployment completed!"
    echo ""
    echo "To view status: kubectl get pods -n factorybrain"
    echo "To view logs: kubectl logs -f deployment/factorybrain-backend -n factorybrain"
    echo "To get service URL: kubectl get ingress -n factorybrain"
    echo ""
else
    echo "Invalid option selected."
    exit 1
fi