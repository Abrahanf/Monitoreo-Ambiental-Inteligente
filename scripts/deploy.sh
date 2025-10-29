# ========================================
# scripts/deploy.sh
# ========================================
#!/bin/bash

echo "=== Despliegue en AWS ==="

# Variables
AWS_REGION="us-east-1"
ECR_REGISTRY="YOUR_ECR_REGISTRY"
CLUSTER_NAME="environmental-monitoring-cluster"
SERVICE_NAME="environmental-monitoring-service"

# 1. Build y push de imágenes Docker
echo "📦 Construyendo imágenes..."

# Backend
cd backend
docker build -t environmental-monitoring-backend .
docker tag environmental-monitoring-backend:latest $ECR_REGISTRY/backend:latest
docker push $ECR_REGISTRY/backend:latest

# IA Service
cd ../ia-service
docker build -t environmental-monitoring-ia .
docker tag environmental-monitoring-ia:latest $ECR_REGISTRY/ia-service:latest
docker push $ECR_REGISTRY/ia-service:latest

echo "✓ Imágenes subidas a ECR"

# 2. Actualizar servicios ECS
echo "🚀 Actualizando servicios ECS..."

aws ecs update-service \
  --cluster $CLUSTER_NAME \
  --service $SERVICE_NAME \
  --force-new-deployment \
  --region $AWS_REGION

echo "✓ Despliegue iniciado"

# 3. Verificar estado
echo "⏳ Esperando despliegue..."
aws ecs wait services-stable \
  --cluster $CLUSTER_NAME \
  --services $SERVICE_NAME \
  --region $AWS_REGION

echo "✅ Despliegue completado exitosamente"

