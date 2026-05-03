# AWS Deployment Guide

Complete guide to deploying CogOS applications to AWS.

## Prerequisites

- AWS account with appropriate permissions
- AWS CLI installed and configured
- kubectl installed
- Docker installed
- Basic AWS knowledge

---

## Quick Start

### 1. Create EKS Cluster

```python
from cogos import CogOS

cogos = CogOS()

# Create EKS cluster infrastructure
result = cogos.think("""
Create AWS EKS cluster with:
- VPC with public/private subnets
- EKS cluster (version 1.28+)
- Node groups (mixed instance types)
- Security groups
- IAM roles
- EBS CSI driver
""", modules=["aws", "kubernetes", "terraform"])

print(result.terraform)  # Terraform configuration
print(result.outputs)  # Cluster endpoint, etc.
```

### 2. Deploy Application

```python
# Deploy to EKS
deployment = cogos.think("""
Deploy Python FastAPI application to EKS:
- Docker container image
- Kubernetes manifests
- LoadBalancer service
- Ingress with ALB
- ConfigMaps and Secrets
- HPA for scaling
""", modules=["python", "fastapi", "kubernetes", "aws"])
```

---

## Infrastructure Options

### Option 1: ECS (Elastic Container Service)

```python
# Create ECS deployment
result = cogos.think("""
Create ECS deployment with:
- ECS cluster
- Fargate tasks
- Application Load Balancer
- Target groups
- ECS task definition
- CloudWatch alarms
- Auto-scaling
""", modules=["aws", "ecs", "docker"])

print(result.task_definition)  # Task definition
print result.service)  # ECS service
print(result.alb)  # ALB configuration
```

**Pros:**
- Serverless containers
- AWS managed
- Easy scaling
- Cost-effective

**Cons:**
- Less control
- AWS vendor lock-in
- Limited to containers

### Option 2: EKS (Elastic Kubernetes Service)

```python
# Create EKS deployment
result = cogos.think("""
Create EKS deployment with:
- EKS cluster
- Node groups
- Application Load Balancer Ingress
- Deployment manifests
- Service accounts
- HPA
- Cluster autoscaler
""", modules=["aws", "kubernetes", "helm"])
```

**Pros:**
- Kubernetes standard
- Portable workloads
- Large ecosystem
- More control

**Cons:**
- More complex
- Higher cost
- Requires Kubernetes knowledge

### Option 3: Serverless (Lambda)

```python
# Create serverless deployment
result = cogos.think("""
Create serverless API with:
- API Gateway
- Lambda functions
- DynamoDB tables
- S3 buckets
- Cognito authentication
- CloudFront distribution
""", modules=["aws", "lambda", "api-gateway"])
```

**Pros:**
- Lowest cost
- No servers to manage
- Auto-scaling
- Pay-per-use

**Cons:**
- Execution limits
- Cold starts
- Vendor lock-in

---

## Complete EKS Deployment

### 1. Infrastructure with Terraform

```python
# Create complete Terraform setup
result = cogos.think("""
Create Terraform configuration for EKS:

# VPC Configuration
- VPC (10.0.0.0/16)
- Public subnets (3 AZs)
- Private subnets (3 AZs)
- NAT gateways
- Internet gateway
- Route tables

# EKS Cluster
- EKS cluster (1.28)
- Managed node groups
- IAM roles
- Security groups
- EBS CSI driver

# Additional Resources
- RDS PostgreSQL
- ElastiCache Redis
- Application Load Balancer
- S3 buckets
- ECR for Docker images
""", modules=["aws", "terraform", "eks"])
```

**Output includes:**
```
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── vpc.tf
├── eks.tf
├── rds.tf
├── elasticache.tf
└── alb.tf
```

### 2. Kubernetes Manifests

```python
# Create Kubernetes manifests
result = cogos.think("""
Create Kubernetes manifests for application:

# Namespace
namespace: production

# Deployment
- Deployment with 3 replicas
- Resource limits
- Liveness/readiness probes
- Environment variables

# Service
- ClusterIP service
- Port configuration

# Ingress
- ALB ingress
- SSL/TLS certificate
- Routing rules

# ConfigMap
- Application config

# Secret
- Database credentials
- API keys

# HPA
- Horizontal Pod Autoscaler
- CPU/memory thresholds
""", modules=["kubernetes", "aws"])
```

**Output includes:**
```
k8s/
├── namespace.yaml
├── deployment.yaml
├── service.yaml
├── ingress.yaml
├── configmap.yaml
├── secret.yaml
└── hpa.yaml
```

### 3. CI/CD Pipeline

```python
# Create GitHub Actions workflow
result = cogos.think("""
Create GitHub Actions workflow for EKS deployment:

name: Deploy to EKS

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    - Checkout code
    - Configure AWS credentials
    - Build Docker image
    - Push to ECR
    - Update kubeconfig
    - Deploy to EKS
    - Run smoke tests
    - Notify on failure
""", modules=["github", "aws", "kubernetes", "docker"])
```

### 4. Monitoring Stack

```python
# Create monitoring setup
result = cogos.think("""
Deploy monitoring stack on EKS:

# Prometheus
- Prometheus deployment
- Service discovery
- Alerting rules

# Grafana
- Grafana deployment
- Datasources
- Dashboards

# Alertmanager
- Alertmanager deployment
- Alert routing
- SNS notifications

# AWS CloudWatch
- Container insights
- Alarms
- Dashboards
""", modules=["prometheus", "grafana", "aws", "kubernetes"])
```

---

## Cost Optimization

### 1. Right-Sizing

```python
# Optimize resource allocation
result = cogos.think("""
Optimize EKS node groups:
- Use mixed instance types
- Right-size instances (t3.medium vs t3.large)
- Enable spot instances
- Auto-scaling based on load
- Cluster autoscaler
""", modules=["aws", "eks", "kubernetes"])
```

### 2. Reserved Instances

```python
# Purchase reserved instances
result = cogos.think("""
Create Reserved Instance plan:
- Analyze usage patterns
- Purchase convertible RIs
- Schedule for renewal
- Track savings
""", modules=["aws", "cost-optimization"])
```

### 3. Lifecycle Policies

```python
# Create lifecycle policies
result = cogos.think("""
Create cost-saving lifecycle policies:
- EBS snapshot lifecycle
- S3 lifecycle rules
- ECR image cleanup
- CloudWatch logs retention
""", modules=["aws", "s3", "ecr"])
```

---

## Security

### 1. Network Security

```python
# Secure network configuration
result = cogos.think("""
Create secure network setup:
- VPC with private subnets
- Security groups (least privilege)
- Network ACLs
- NAT gateways (not internet gateways)
- VPC endpoints (AWS services)
- PrivateLink for ECR
""", modules=["aws", "security", "vpc"])
```

### 2. Secrets Management

```python
# Implement secrets management
result = cogos.think("""
Implement secrets management:
- AWS Secrets Manager
- IAM roles for service accounts
- Encrypted environment variables
- Rotation policies
- Kubernetes secrets (encrypted)
""", modules=["aws", "secrets-manager", "kubernetes"])
```

### 3. Compliance

```python
# Create compliance setup
result = cogos.think("""
Implement AWS compliance features:
- AWS Config rules
- CloudTrail logging
- GuardDuty security
- Security Hub
- AWS Audit Manager
""", modules=["aws", "compliance", "security"])
```

---

## Disaster Recovery

### 1. Backup Strategy

```python
# Create backup strategy
result = cogos.think("""
Create comprehensive backup strategy:
- RDS automated backups (7 days)
- RDS snapshots (daily, retained 30 days)
- EBS snapshots (daily)
- S3 versioning
- Cross-region replication
""", modules=["aws", "rds", "ebs", "s3"])
```

### 2. Multi-Region Setup

```python
# Create multi-region deployment
result = cogos.think("""
Design multi-region architecture:
- Active-active regions
- Route53 routing
- Database replication
- Data synchronization
- Failover procedures
- Health checks
""", modules=["aws", "route53", "rds", "kubernetes"])
```

---

## Example: Complete EKS Deployment

```python
# Deploy complete application to EKS
cogos = CogOS()

# 1. Create infrastructure
infrastructure = cogos.think("""
Create AWS infrastructure for EKS:
- VPC (10.0.0.0/16)
- 3 public subnets
- 3 private subnets
- NAT gateways
- EKS cluster (1.28)
- Managed node groups (t3.medium)
- RDS PostgreSQL (db.t3.micro)
- ElastiCache Redis (cache.t3.micro)
- ALB
- ECR repository
""", modules=["aws", "eks", "terraform"])

# 2. Build and push Docker image
docker = cogos.think("""
Create Docker setup:
- Multi-stage Dockerfile
- Build and test image
- Tag for ECR
- Push to ECR
""", modules=["docker", "aws"], context=infrastructure)

# 3. Deploy to EKS
deployment = cogos.think("""
Deploy to EKS:
- Namespace
- Deployment (3 replicas)
- Service (ClusterIP)
- Ingress (ALB with SSL)
- ConfigMap (environment)
- Secret (credentials)
- HPA (min 3, max 10)
""", modules=["kubernetes", "aws", "helm"], context=infrastructure)

# 4. Set up monitoring
monitoring = cogos.think("""
Deploy monitoring stack:
- Prometheus
- Grafana
- Alertmanager
- CloudWatch Container Insights
- Custom dashboards
- Alert rules
""", modules=["prometheus", "grafana", "aws", "kubernetes"], context=infrastructure)

# 5. Set up CI/CD
cicd = cogos.think("""
Create GitHub Actions workflow:
- Build Docker image
- Run tests
- Push to ECR
- Deploy to EKS
- Run smoke tests
- Notify on failure
""", modules=["github", "aws", "docker", "kubernetes"], context=infrastructure)
```

---

## Best Practices

1. **Use Infrastructure as Code** - Terraform or CloudFormation
2. **Implement GitOps** - Use GitOps for deployments
3. **Enable monitoring** - Prometheus, Grafana, CloudWatch
4. **Set up alerts** - Alertmanager, SNS notifications
5. **Use tags** - Tag all AWS resources
6. **Enable logging** - CloudTrail, CloudWatch Logs
7. **Secure secrets** - AWS Secrets Manager, not plain text
8. **Auto-scaling** - HPA, Cluster Autoscaler
9. **Cost optimization** - Right-size instances, use spot
10. **Disaster recovery** - Backups, multi-region

---

## Troubleshooting

### Cluster Issues

```bash
# Check cluster status
kubectl cluster-info
kubectl get nodes

# Check pods
kubectl get pods -A
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>
```

### Deployment Issues

```bash
# Check deployment
kubectl get deployments
kubectl describe deployment <deployment-name>

# Rollback
kubectl rollout undo deployment <deployment-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

### Networking Issues

```bash
# Check services
kubectl get services
kubectl describe service <service-name>

# Check ingress
kubectl get ingress
kubectl describe ingress <ingress-name>

# Test connectivity
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- curl <service-name>
```

---

## Resources

- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/)
- [EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

**Next:** [GCP Deployment Guide](deployment_gcp.md)
