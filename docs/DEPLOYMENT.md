# ========================================
# docs/DEPLOYMENT.md
# ========================================

# 📘 Guía de Despliegue en AWS

## Requisitos previos
- Cuenta AWS activa
- AWS CLI instalado y configurado
- Docker instalado
- Terraform (opcional)

## Arquitectura en AWS

```
Internet
   │
   ├─ Route 53 (DNS)
   │
   ├─ CloudFront (CDN) ─→ S3 (Frontend estático)
   │
   ├─ Application Load Balancer
   │   │
   │   ├─ ECS Fargate (Backend)
   │   └─ ECS Fargate (IA Service)
   │
   ├─ RDS MySQL (Base de datos)
   │
   ├─ IoT Core (MQTT)
   │
   ├─ S3 (Reportes PDF)
   │
   └─ CloudWatch (Logs y métricas)
```

## Pasos de despliegue

### 1. Crear Base de Datos RDS

```bash
# Via AWS Console o CLI
aws rds create-db-instance \
  --db-instance-identifier env-monitoring-db \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --master-username admin \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-xxxxx \
  --db-subnet-group-name your-subnet-group
```

### 2. Configurar ECR (Elastic Container Registry)

```bash
# Crear repositorios
aws ecr create-repository --repository-name environmental-monitoring/backend
aws ecr create-repository --repository-name environmental-monitoring/ia-service

# Login a ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin YOUR_ECR_URL
```

### 3. Subir imágenes Docker

```bash
# Build y push
./scripts/deploy.sh
```

### 4. Crear Cluster ECS con Fargate

```bash
# Crear cluster
aws ecs create-cluster --cluster-name environmental-monitoring-cluster

# Crear task definition (ver task-definition.json)
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Crear servicio
aws ecs create-service \
  --cluster environmental-monitoring-cluster \
  --service-name env-monitoring-service \
  --task-definition env-monitoring:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### 5. Configurar AWS IoT Core (MQTT)

```bash
# Crear thing
aws iot create-thing --thing-name ESP32-Central

# Crear certificados
aws iot create-keys-and-certificate \
  --set-as-active \
  --certificate-pem-outfile esp32-cert.pem \
  --public-key-outfile esp32-public.key \
  --private-key-outfile esp32-private.key

# Crear policy y attachar
aws iot create-policy --policy-name ESP32-Policy --policy-document file://iot-policy.json
aws iot attach-policy --policy-name ESP32-Policy --target CERTIFICATE_ARN
```

### 6. Variables de entorno

Configurar en ECS Task Definition o usar AWS Secrets Manager:

```json
{
  "DATABASE_URL": "mysql+pymysql://user:pass@rds-endpoint:3306/db",
  "JWT_SECRET_KEY": "from-secrets-manager",
  "MQTT_BROKER_URL": "xxx.iot.us-east-1.amazonaws.com",
  "S3_BUCKET": "environmental-reports-bucket"
}
```

## Monitoreo

- CloudWatch Logs: `/ecs/environmental-monitoring`
- CloudWatch Metrics: CPU, memoria, requests
- CloudWatch Alarms: Configurar alertas

## Costos estimados (mensual)

- RDS db.t3.micro: ~$15
- ECS Fargate (2 tareas): ~$30
- ALB: ~$20
- S3: ~$1
- IoT Core: ~$2
- **Total aprox: $70/mes**