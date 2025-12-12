# FactoryBrain AI - Deployment Guide

## Deployment Options

This guide covers three deployment methods:
1. Local Development (Docker Compose)
2. Production Kubernetes (Vultr)
3. Manual Installation (Bare Metal)

## Prerequisites

### All Deployments
- Git
- API Keys (ElevenLabs, Cerebras, Anthropic, Raindrop, Vultr)

### Docker Compose
- Docker 20.10+
- Docker Compose 2.0+
- 8GB RAM minimum
- 20GB disk space

### Kubernetes
- kubectl 1.24+
- Kubernetes cluster access
- Helm 3.0+ (optional)
- 16GB RAM minimum per node
- 50GB disk space

### Manual Installation
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Node.js 18+ (for frontend development)
- 8GB RAM minimum
- 20GB disk space

## Method 1: Docker Compose Deployment

### Step 1: Clone Repository
```bash
git clone https://github.com/samirasamrose/factorybrain-ai.git
cd factorybrain-ai
```

### Step 2: Configure Environment
```bash
cp deployment/.env.template deployment/.env
nano deployment/.env
```

Required environment variables:
```env
ELEVENLABS_API_KEY=sk-elevenlabs-xxxxx
CEREBRAS_API_KEY=csk-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx
RAINDROP_BUCKET_ENDPOINT=https://buckets.raindrop.io
RAINDROP_SQL_ENDPOINT=https://sql.raindrop.io
RAINDROP_MEMORY_ENDPOINT=https://memory.raindrop.io
RAINDROP_INFERENCE_ENDPOINT=https://inference.raindrop.io
VULTR_ACCESS_KEY=your_access_key
VULTR_SECRET_KEY=your_secret_key
SECRET_KEY=generate_32_char_random_string_here
```

### Step 3: Build and Start Services
```bash
cd deployment
docker-compose up -d
```

### Step 4: Verify Deployment
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend

# Test API
curl http://localhost:8000/health
```

Expected health response:
```json
{
  "status": "healthy",
  "timestamp": "2024-12-08T10:30:00Z",
  "services": {
    "api": "operational",
    "database": "operational",
    "cerebras": "operational",
    "raindrop": "operational",
    "iot_broker": "operational"
  }
}
```

### Step 5: Initialize Database
```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Seed initial data (optional)
docker-compose exec backend python -m backend.app.seed_data
```

### Step 6: Access Application

- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- MQTT Broker: localhost:1883

Default login credentials:
- Admin: `admin` / `admin123`
- Supervisor: `supervisor` / `super123`
- Operator: `operator` / `oper123`

### Step 7: Train ML Models
```bash
# From host machine
./scripts/train_models.sh

# Or from inside container
docker-compose exec backend python ml_models/anomaly_detection/train.py
docker-compose exec backend python ml_models/predictive_maintenance/train.py
docker-compose exec backend python ml_models/energy_optimization/train.py
```

### Maintenance Commands
```bash
# Stop services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# View logs
docker-compose logs -f [service_name]

# Restart service
docker-compose restart backend

# Scale backend workers
docker-compose up -d --scale backend=3

# Backup database
docker-compose exec postgres pg_dump -U factorybrain factorybrain > backup.sql

# Restore database
docker-compose exec -T postgres psql -U factorybrain factorybrain < backup.sql
```

## Method 2: Kubernetes Deployment (Vultr)

### Step 1: Set Up Vultr Kubernetes Cluster
```bash
# Install Vultr CLI
curl -L https://github.com/vultr/vultr-cli/releases/latest/download/vultr-cli-linux-amd64.tar.gz | tar xz
sudo mv vultr-cli /usr/local/bin/

# Configure Vultr CLI
vultr-cli configure

# Create Kubernetes cluster
vultr-cli kubernetes create \
  --label factorybrain-production \
  --region ewr \
  --version v1.28.0 \
  --node-pools "quantity=3,plan=vc2-2c-4gb,label=worker-pool"

# Get cluster ID
CLUSTER_ID=$(vultr-cli kubernetes list | grep factorybrain | awk '{print $1}')

# Download kubeconfig
vultr-cli kubernetes config $CLUSTER_ID > ~/.kube/factorybrain-config
export KUBECONFIG=~/.kube/factorybrain-config

# Verify connection
kubectl get nodes
```

### Step 2: Create Kubernetes Secrets
```bash
# Create namespace
kubectl create namespace factorybrain

# Create secrets
kubectl create secret generic factorybrain-secrets \
  --from-literal=database-url='postgresql://factorybrain:CHANGE_PASSWORD@postgres-service:5432/factorybrain' \
  --from-literal=redis-url='redis://redis-service:6379' \
  --from-literal=elevenlabs-api-key='sk-elevenlabs-xxxxx' \
  --from-literal=cerebras-api-key='csk-xxxxx' \
  --from-literal=anthropic-api-key='sk-ant-xxxxx' \
  --from-literal=raindrop-bucket-endpoint='https://buckets.raindrop.io' \
  --from-literal=raindrop-sql-endpoint='https://sql.raindrop.io' \
  --from-literal=raindrop-memory-endpoint='https://memory.raindrop.io' \
  --from-literal=raindrop-inference-endpoint='https://inference.raindrop.io' \
  --from-literal=vultr-access-key='your_access_key' \
  --from-literal=vultr-secret-key='your_secret_key' \
  --from-literal=secret-key='generate_32_char_random_string' \
  -n factorybrain
```

### Step 3: Build and Push Docker Images
```bash
# Build images
docker build -f backend/Dockerfile -t factorybrain/backend:latest .
docker build -f frontend/Dockerfile -t factorybrain/frontend:latest .

# Tag for registry (use your registry)
docker tag factorybrain/backend:latest registry.example.com/factorybrain/backend:latest
docker tag factorybrain/frontend:latest registry.example.com/factorybrain/frontend:latest

# Push to registry
docker push registry.example.com/factorybrain/backend:latest
docker push registry.example.com/factorybrain/frontend:latest

# Or use Docker Hub
docker login
docker tag factorybrain/backend:latest samirasamrose/factorybrain-backend:latest
docker tag factorybrain/frontend:latest samirasamrose/factorybrain-frontend:latest
docker push samirasamrose/factorybrain-backend:latest
docker push samirasamrose/factorybrain-frontend:latest
```

Update image references in deployment files to match registry.

### Step 4: Deploy Database
```bash
# Deploy PostgreSQL
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: factorybrain
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: factorybrain
spec:
  serviceName: postgres-service
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        env:
        - name: POSTGRES_USER
          value: factorybrain
        - name: POSTGRES_PASSWORD
          value: CHANGE_PASSWORD
        - name: POSTGRES_DB
          value: factorybrain
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
EOF

# Deploy Redis
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: factorybrain
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
EOF
```

### Step 5: Deploy Application
```bash
# Apply all Kubernetes manifests
kubectl apply -f deployment/kubernetes/namespace.yaml
kubectl apply -f deployment/kubernetes/backend-deployment.yaml
kubectl apply -f deployment/kubernetes/frontend-deployment.yaml
kubectl apply -f deployment/kubernetes/ml-worker-deployment.yaml
kubectl apply -f deployment/kubernetes/services.yaml
kubectl apply -f deployment/kubernetes/ingress.yaml
```

### Step 6: Configure Ingress
```bash
# Install nginx ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# Install cert-manager for SSL
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer for Let's Encrypt
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Update DNS records to point to ingress IP
kubectl get ingress -n factorybrain
# Point factorybrain.example.com and api.factorybrain.example.com to EXTERNAL-IP
```

### Step 7: Initialize Database
```bash
# Get backend pod name
POD_NAME=$(kubectl get pods -n factorybrain -l app=factorybrain-backend -o jsonpath='{.items[0].metadata.name}')

# Run migrations
kubectl exec -n factorybrain $POD_NAME -- alembic upgrade head

# Train models
kubectl exec -n factorybrain $POD_NAME -- python ml_models/anomaly_detection/train.py
kubectl exec -n factorybrain $POD_NAME -- python ml_models/predictive_maintenance/train.py
kubectl exec -n factorybrain $POD_NAME -- python ml_models/energy_optimization/train.py
```

### Step 8: Verify Deployment
```bash
# Check pod status
kubectl get pods -n factorybrain

# Check services
kubectl get services -n factorybrain

# Check ingress
kubectl get ingress -n factorybrain

# View logs
kubectl logs -f deployment/factorybrain-backend -n factorybrain

# Test health endpoint
curl https://api.factorybrain.example.com/health
```

### Maintenance Commands
```bash
# Scale deployment
kubectl scale deployment factorybrain-backend --replicas=5 -n factorybrain

# Update image
kubectl set image deployment/factorybrain-backend backend=samirasamrose/factorybrain-backend:v1.1 -n factorybrain

# Rollback deployment
kubectl rollout undo deployment/factorybrain-backend -n factorybrain

# View rollout history
kubectl rollout history deployment/factorybrain-backend -n factorybrain

# Backup database
kubectl exec -n factorybrain postgres-0 -- pg_dump -U factorybrain factorybrain > backup.sql

# Port forward for debugging
kubectl port-forward -n factorybrain service/factorybrain-backend-service 8000:8000

# Execute commands in pod
kubectl exec -it -n factorybrain $POD_NAME -- /bin/bash

# Delete deployment
kubectl delete namespace factorybrain
```

## Method 3: Manual Installation

### Step 1: Install System Dependencies

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql-15 redis-server nginx
```

#### CentOS/RHEL
```bash
sudo yum install -y python3.11 postgresql15 redis nginx
```

#### macOS
```bash
brew install python@3.11 postgresql@15 redis nginx
```

### Step 2: Set Up Database
```bash
# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql <<EOF
CREATE DATABASE factorybrain;
CREATE USER factorybrain WITH PASSWORD 'factory_secure_pass';
GRANT ALL PRIVILEGES ON DATABASE factorybrain TO factorybrain;
\q
EOF
```

### Step 3: Set Up Redis
```bash
# Start Redis
sudo systemctl start redis
sudo systemctl enable redis

# Verify Redis is running
redis-cli ping
# Should return: PONG
```

### Step 4: Clone and Configure
```bash
# Clone repository
git clone https://github.com/samirasamrose/factorybrain-ai.git
cd factorybrain-ai

# Run setup script
chmod +x scripts/*.sh
./scripts/setup.sh

# Configure environment
cp deployment/.env.template deployment/.env
nano deployment/.env
```

### Step 5: Install Python Dependencies
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Step 6: Initialize Database
```bash
# Set database URL
export DATABASE_URL="postgresql://factorybrain:factory_secure_pass@localhost:5432/factorybrain"

# Run migrations
cd backend
alembic upgrade head
cd ..
```

### Step 7: Download Datasets and Train Models
```bash
# Download datasets
./scripts/data_download.sh

# Train models
./scripts/train_models.sh
```

### Step 8: Start Backend
```bash
# Start backend with uvicorn
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
cd ..
```

### Step 9: Configure Nginx for Frontend
```bash
# Create nginx configuration
sudo nano /etc/nginx/sites-available/factorybrain

# Add configuration:
server {
    listen 80;
    server_name localhost;
    root /path/to/factorybrain-ai/frontend/templates;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /static/ {
        alias /path/to/factorybrain-ai/frontend/static/;
        expires 30d;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/factorybrain /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 10: Set Up Systemd Services

Create backend service:
```bash
sudo nano /etc/systemd/system/factorybrain-backend.service
```

Add content:
```ini
[Unit]
Description=FactoryBrain AI Backend
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=samirasamrose
WorkingDirectory=/path/to/factorybrain-ai/backend
Environment="PATH=/path/to/factorybrain-ai/venv/bin"
Environment="DATABASE_URL=postgresql://factorybrain:factory_secure_pass@localhost:5432/factorybrain"
ExecStart=/path/to/factorybrain-ai/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable factorybrain-backend
sudo systemctl start factorybrain-backend
sudo systemctl status factorybrain-backend
```

### Step 11: Verify Installation
```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost

# View logs
sudo journalctl -u factorybrain-backend -f
```

## Post-Deployment Tasks

### 1. Change Default Passwords
```bash
# Connect to database
psql -U factorybrain -d factorybrain

# Update admin password
UPDATE users SET password = 'new_hashed_password' WHERE username = 'admin';
```

Or use the API to create new users.

### 2. Configure Firewall
```bash
# Ubuntu/Debian
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### 3. Set Up SSL Certificate
```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d factorybrain.example.com -d api.factorybrain.example.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

### 4. Configure Backup Cron Job
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/factorybrain-ai/scripts/backup.sh
```

Create backup script:
```bash
nano scripts/backup.sh
```
```bash
#!/bin/bash
BACKUP_DIR="/backups/factorybrain"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U factorybrain factorybrain > $BACKUP_DIR/db_$DATE.sql

# Backup ML models
tar -czf $BACKUP_DIR/models_$DATE.tar.gz ml_models/saved/

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
```
```bash
chmod +x scripts/backup.sh
```

### 5. Monitor Application

Install monitoring tools:
```bash
# Prometheus + Grafana
docker run -d -p 9090:9090 --name prometheus prom/prometheus
docker run -d -p 3000:3000 --name grafana grafana/grafana
```

Configure Prometheus to scrape FastAPI metrics.

### 6. Set Up Log Rotation
```bash
sudo nano /etc/logrotate.d/factorybrain
```
```
/path/to/factorybrain-ai/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 samirasamrose samirasamrose
    sharedscripts
    postrotate
        systemctl reload factorybrain-backend > /dev/null
    endscript
}
```

## Troubleshooting

### Backend Won't Start
```bash
# Check logs
sudo journalctl -u factorybrain-backend -n 50

# Common issues:
# 1. Database connection
psql -U factorybrain -d factorybrain -c "SELECT 1;"

# 2. Port already in use
sudo lsof -i :8000
sudo kill -9 <PID>

# 3. Missing dependencies
source venv/bin/activate
pip install -r backend/requirements.txt

# 4. Environment variables
cat deployment/.env
```

### Database Connection Errors
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U factorybrain -d factorybrain

# Check pg_hba.conf
sudo nano /etc/postgresql/15/main/pg_hba.conf
# Ensure: local   all   factorybrain   md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### ML Models Not Loading
```bash
# Check model files exist
ls -la ml_models/saved/

# Retrain if missing
./scripts/train_models.sh

# Check permissions
chmod -R 755 ml_models/
```

### High Memory Usage
```bash
# Check memory
free -h

# Reduce backend workers
# Edit systemd service or docker-compose to use fewer workers

# Enable swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Frontend Not Loading
```bash
# Check nginx status
sudo systemctl status nginx

# Test nginx configuration
sudo nginx -t

# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Verify file permissions
ls -la frontend/templates/
ls -la frontend/static/
```

## Performance Tuning

### PostgreSQL
```bash
sudo nano /etc/postgresql/15/main/postgresql.conf
```
```
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
```

### Uvicorn Workers
```bash
# Start with multiple workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Nginx
```bash
sudo nano /etc/nginx/nginx.conf
```
```
worker_processes auto;
worker_connections 1024;

gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css application/json application/javascript text/xml;

client_max_body_size 20M;
```

## Security Hardening

### 1. Disable Root Login
```bash
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
sudo systemctl restart sshd
```

### 2. Configure Fail2Ban
```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Enable AppArmor/SELinux
```bash
# Ubuntu
sudo systemctl enable apparmor
sudo systemctl start apparmor

# CentOS
sudo setenforce 1
```

### 4. Regular Updates
```bash
# Ubuntu
sudo apt update && sudo apt upgrade -y

# CentOS
sudo yum update -y
```

## Scaling Guidelines

### Horizontal Scaling

- Add more backend pods/containers
- Use load balancer (nginx, HAProxy)
- Implement session affinity for WebSockets
- Scale ML workers independently

### Vertical Scaling

- Increase memory allocation
- Add more CPU cores
- Upgrade database instance
- Use SSD storage for better I/O

### Database Scaling

- Implement read replicas
- Use connection pooling (PgBouncer)
- Partition large tables
- Optimize indexes
