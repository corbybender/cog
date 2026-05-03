# GCP Deployment Guide

Complete guide to deploying CogOS applications to Google Cloud Platform.

## Prerequisites

- GCP account with appropriate permissions
- gcloud CLI installed and configured
- kubectl installed
- Docker installed
- Basic GCP knowledge

---

## Quick Start

### 1. Create GKE Cluster

```python
from cogos import CogOS

cogos = CogOS()

# Create GKE cluster
result = cogos.think("""
Create GCP GKE cluster with:
- VPC network
- Subnets (3 regions)
- GKE cluster (1.28+)
- Node pools (e2-medium)
- IAM roles
- Cloud Router
- Cloud NAT
""", modules=["gcp", "kubernetes", "terraform"])

print(result.terraform)  # Terraform configuration
print(result.outputs)  # Cluster endpoint, etc.
```

### 2. Deploy Application

```python
# Deploy to GKE
deployment = cogos.think("""
Deploy Python FastAPI application to GKE:
- Docker container image
- Kubernetes manifests
- Service (LoadBalancer)
- Ingress with Cloud Armor
- ConfigMaps and Secrets
- HPA for scaling
""", modules=["python", "fastapi", "kubernetes", "gcp"])
```

---

## Infrastructure Options

### Option 1: Cloud Run (Serverless)

```python
# Create Cloud Run deployment
result = cogos.think("""
Create Cloud Run deployment with:
- Cloud Run service
- Container image
- Auto-scaling (0-1000 instances)
- Cloud SQL connection
- Cloud Storage
- Cloud Armor security
- Custom domain
""", modules=["gcp", "cloud-run", "docker"])

print(result.service)  # Cloud Run service
print result.yaml)  # Service configuration
```

**Pros:**
- Fully serverless
- Auto-scaling to zero
- Pay-per-use
- Managed infrastructure

**Cons:**
- Execution limits
- Cold starts
- Less control

### Option 2: GKE (Google Kubernetes Engine)

```python
# Create GKE deployment
result = cogos.think("""
Create GKE deployment with:
- GKE cluster (Autopilot)
- Node pools
- Cloud Load Balancing
- Cloud Armor
- Cloud CDN
- Deployment manifests
- HPA
""", modules=["gcp", "kubernetes", "helm"])
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

### Option 3: App Engine

```python
# Create App Engine deployment
result = cogos.think("""
Create App Engine deployment with:
- App Engine service
- Flexible or Standard runtime
- Cloud SQL
- Cloud Memorystore
- Cloud Tasks
- Traffic splitting
""", modules=["gcp", "app-engine", "python"])
```

---

## Complete GKE Deployment

### 1. Infrastructure with Terraform

```python
# Create Terraform setup
result = cogos.think("""
Create Terraform configuration for GKE:

# VPC Configuration
- VPC (custom network)
- Subnets (3 regions)
- Cloud Router
- Cloud NAT
- Firewall rules

# GKE Cluster
- GKE cluster (Autopilot)
- Node pools
- IAM service accounts
- Cloud Armor security policy

# Additional Resources
- Cloud SQL PostgreSQL
- Cloud Memorystore (Redis)
- Cloud Load Balancer
- Cloud Storage buckets
- Artifact Registry for images
""", modules=["gcp", "terraform", "gke"])
```

**Output includes:**
```
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── vpc.tf
├── gke.tf
├── cloudsql.tf
├── memorystore.tf
└── lb.tf
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
- LoadBalancer service (GCP)

# Ingress
- GKE Ingress
- Cloud Armor
- Static IP
- SSL certificate

# ConfigMap
- Application config

# Secret
- Database credentials
- API keys

# HPA
- Horizontal Pod Autoscaler
- CPU/memory thresholds
""", modules=["kubernetes", "gcp"])
```

### 3. CI/CD Pipeline

```python
# Create Cloud Build pipeline
result = cogos.think("""
Create Cloud Build pipeline for GKE:

steps:
  - Build Docker image
  - Run tests
  - Push to Artifact Registry
  - Deploy to GKE
  - Run smoke tests
  - Create new tag
""", modules=["gcp", "cloud-build", "kubernetes", "docker"])
```

### 4. Monitoring Stack

```python
# Create monitoring setup
result = cogos.think("""
Deploy monitoring stack on GKE:

# Cloud Monitoring
- Metrics collection
- Dashboards
- Alerting policies
- Uptime checks

# Cloud Logging
- Log collection
- Log sinks
- Log-based metrics

# Optional: Prometheus + Grafana
- Prometheus deployment
- Grafana deployment
- Custom dashboards
""", modules=["gcp", "monitoring", "prometheus", "grafana"])
```

---

## Cost Optimization

### 1. Right-Sizing

```python
# Optimize resource allocation
result = cogos.think("""
Optimize GKE resources:
- Use Autopilot (automatic right-sizing)
- Use preemptible VMs
- Enable cluster autoscaler
- Set resource limits
- Use spot VMs for workloads
""", modules=["gcp", "gke", "kubernetes"])
```

### 2. Committed Use Discounts

```python
# Create commitment plan
result = cogos.think("""
Create committed use discounts:
- Analyze usage patterns
- Purchase committed use
- Schedule for renewal
- Track savings
""", modules=["gcp", "cost-optimization"])
```

### 3. Lifecycle Policies

```python
# Create lifecycle policies
result = cogos.think("""
Create cost-saving lifecycle policies:
- Persistent disk snapshots
- Cloud Storage lifecycle
- Artifact Registry cleanup
- Cloud Logging retention
""", modules=["gcp", "storage", "artifact-registry"])
```

---

## Security

### 1. Network Security

```python
# Secure network configuration
result = cogos.think("""
Create secure network setup:
- VPC with private clusters
- Firewall rules (least privilege)
- Cloud Armor policies
- Cloud NAT (not public IPs)
- Private Service Connect
- VPC Service Controls
""", modules=["gcp", "security", "vpc"])
```

### 2. Secrets Management

```python
# Implement secrets management
result = cogos.think("""
Implement secrets management:
- Secret Manager
- IAM roles for service accounts
- Workload Identity
- Encrypted environment variables
- Rotation policies
""", modules=["gcp", "secret-manager", "kubernetes"])
```

### 3. Compliance

```python
# Create compliance setup
result = cogos.think("""
Implement GCP compliance features:
- Asset Inventory
- Security Command Center
- Audit Logs
- Policy Controller
- Assured Workloads
""", modules=["gcp", "compliance", "security"])
```

---

## Disaster Recovery

### 1. Backup Strategy

```python
# Create backup strategy
result = cogos.think("""
Create comprehensive backup strategy:
- Cloud SQL automated backups
- Cloud SQL exports (daily)
- Persistent disk snapshots
- Cloud Storage versioning
- Cross-region replication
""", modules=["gcp", "cloudsql", "storage"])
```

### 2. Multi-Region Setup

```python
# Create multi-region deployment
result = cogos.think("""
Design multi-region architecture:
- Multi-region clusters
- Cloud DNS routing
- Database replication
- Data synchronization
- Failover procedures
- Health checks
""", modules=["gcp", "cloud-dns", "cloudsql", "kubernetes"])
```

---

## Example: Complete GKE Deployment

```python
# Deploy complete application to GKE
cogos = CogOS()

# 1. Create infrastructure
infrastructure = cogos.think("""
Create GCP infrastructure for GKE:
- VPC (custom network)
- 3 subnets (different regions)
- Cloud Router
- Cloud NAT
- GKE cluster (Autopilot)
- Cloud SQL PostgreSQL
- Cloud Memorystore Redis
- Cloud Load Balancer
- Artifact Registry
""", modules=["gcp", "gke", "terraform"])

# 2. Build and push Docker image
docker = cogos.think("""
Create Docker setup:
- Multi-stage Dockerfile
- Build and test image
- Tag for Artifact Registry
- Push to Artifact Registry
""", modules=["docker", "gcp"], context=infrastructure)

# 3. Deploy to GKE
deployment = cogos.think("""
Deploy to GKE:
- Namespace
- Deployment (3 replicas)
- Service (LoadBalancer)
- Ingress (Cloud Armor + SSL)
- ConfigMap (environment)
- Secret (credentials)
- HPA (min 3, max 10)
""", modules=["kubernetes", "gcp", "helm"], context=infrastructure)

# 4. Set up monitoring
monitoring = cogos.think("""
Deploy monitoring stack:
- Cloud Monitoring
- Cloud Logging
- Cloud Dashboards
- Alerting policies
- Uptime checks
""", modules=["gcp", "monitoring"], context=infrastructure)

# 5. Set up CI/CD
cicd = cogos.think("""
Create Cloud Build pipeline:
- Build Docker image
- Run tests
- Push to Artifact Registry
- Deploy to GKE
- Run smoke tests
- Notify on failure
""", modules=["gcp", "cloud-build", "docker", "kubernetes"], context=infrastructure)
```

---

## Best Practices

1. **Use Infrastructure as Code** - Terraform or Deployment Manager
2. **Use GKE Autopilot** - Let GCP manage nodes
3. **Enable monitoring** - Cloud Monitoring, Logging
4. **Set up alerts** - Alert policies, notification channels
5. **Use labels** - Label all GCP resources
6. **Enable logging** - Cloud Audit Logs, Cloud Logging
7. **Secure secrets** - Secret Manager, not plain text
8. **Auto-scaling** - HPA, Cluster Autoscaler
9. **Cost optimization** - Use preemptible, right-size
10. **Disaster recovery** - Backups, multi-region

---

## Troubleshooting

### Cluster Issues

```bash
# Check cluster status
gcloud container clusters list
gcloud container clusters describe CLUSTER_NAME

# Check nodes
kubectl get nodes
kubectl describe node <node-name>

# Check pods
kubectl get pods -A
kubectl describe pod <pod-name>
```

### Deployment Issues

```bash
# Check deployment
kubectl get deployments
kubectl describe deployment <deployment-name>

# Check logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>

# Rollback
kubectl rollout undo deployment <deployment-name>
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

- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [GCP Best Practices](https://cloud.google.com/architecture/best-practices)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

---

**Next:** [Azure Deployment Guide](deployment_azure.md)
