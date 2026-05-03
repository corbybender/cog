# Azure Deployment Guide

Complete guide to deploying CogOS applications to Microsoft Azure.

## Prerequisites

- Azure account with appropriate permissions
- Azure CLI installed and configured
- kubectl installed
- Docker installed
- Basic Azure knowledge

---

## Quick Start

### 1. Create AKS Cluster

```python
from cogos import CogOS

cogos = CogOS()

# Create AKS cluster
result = cogos.think("""
Create Azure AKS cluster with:
- Resource group
- VNet network
- Subnets
- AKS cluster (1.28+)
- Node pools (Standard_DS2_v2)
- Azure AD integration
- Azure Monitor
""", modules=["azure", "kubernetes", "terraform"])

print(result.terraform)  # Terraform configuration
print(result.outputs)  # Cluster endpoint, etc.
```

### 2. Deploy Application

```python
# Deploy to AKS
deployment = cogos.think("""
Deploy Python FastAPI application to AKS:
- Docker container image
- Kubernetes manifests
- Service (LoadBalancer)
- Ingress with Application Gateway
- ConfigMaps and Secrets
- HPA for scaling
""", modules=["python", "fastapi", "kubernetes", "azure"])
```

---

## Infrastructure Options

### Option 1: Container Instances

```python
# Create Container Instances deployment
result = cogos.think("""
Create Azure Container Instances with:
- Container group
- Container image
- Auto-scaling
- Azure Files mount
- Azure Key Vault
- DNS label
""", modules=["azure", "container-instances", "docker"])

print(result.deployment)  # Container instance
print result.yaml)  # Deployment YAML
```

**Pros:**
- Fastest deployment
- Pay-per-second
- No management overhead
- Simple

**Cons:**
- No orchestration
- Limited scaling
- Single containers
- No advanced features

### Option 2: AKS (Azure Kubernetes Service)

```python
# Create AKS deployment
result = cogos.think("""
Create AKS deployment with:
- AKS cluster
- Node pools
- Application Gateway ingress
- Azure Policy
- Azure Monitor
- Deployment manifests
- HPA
""", modules=["azure", "kubernetes", "helm"])
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

### Option 3: App Service

```python
# Create App Service deployment
result = cogos.think("""
Create App Service deployment with:
- App Service plan
- Web app for containers
- Azure SQL Database
- Azure Cache for Redis
- Application Insights
- Deployment slots
""", modules=["azure", "app-service", "python"])
```

---

## Complete AKS Deployment

### 1. Infrastructure with Terraform

```python
# Create Terraform setup
result = cogos.think("""
Create Terraform configuration for AKS:

# Resource Group
- Resource group
- Location

# VNet Configuration
- VNet (10.0.0.0/16)
- Subnets (3+)
- Network security groups
- Route tables

# AKS Cluster
- AKS cluster (1.28+)
- System node pool
- User node pools
- Azure AD integration
- Managed identities
- Azure Container Registry integration

# Additional Resources
- Azure SQL Database
- Azure Cache for Redis
- Application Gateway
- Azure Container Registry
- Key Vault
- Storage account
""", modules=["azure", "terraform", "aks"])
```

**Output includes:**
```
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── resource_group.tf
├── vnet.tf
├── aks.tf
├── azure_sql.tf
├── redis.tf
└── app_gateway.tf
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
- LoadBalancer service (Azure)

# Ingress
- Application Gateway ingress
- Azure Front Door
- Static IP
- SSL certificate (Azure Key Vault)

# ConfigMap
- Application config

# Secret
- Database credentials (from Key Vault)
- API keys

# HPA
- Horizontal Pod Autoscaler
- CPU/memory thresholds
""", modules=["kubernetes", "azure"])
```

### 3. CI/CD Pipeline

```python
# Create Azure DevOps pipeline
result = cogos.think("""
Create Azure DevOps pipeline for AKS:

trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- Build Docker image
- Run tests
- Push to Azure Container Registry
- Deploy to AKS
- Run smoke tests
- Tag release
""", modules=["azure", "azure-devops", "kubernetes", "docker"])
```

### 4. Monitoring Stack

```python
# Create monitoring setup
result = cogos.think("""
Deploy monitoring stack on AKS:

# Azure Monitor
- Container insights
- Metrics collection
- Dashboards
- Alert rules
- Action groups

# Application Insights
- Application monitoring
- Performance monitoring
- Telemetry

# Optional: Prometheus + Grafana
- Prometheus deployment
- Grafana deployment
- Custom dashboards
""", modules=["azure", "monitoring", "prometheus", "grafana"])
```

---

## Cost Optimization

### 1. Right-Sizing

```python
# Optimize resource allocation
result = cogos.think("""
Optimize AKS resources:
- Right-size VMs
- Use spot instances
- Enable cluster autoscaler
- Set resource limits
- Use burstable VMs (B-series)
""", modules=["azure", "aks", "kubernetes"])
```

### 2. Reserved Instances

```python
# Create reservation plan
result = cogos.think("""
Create Azure reservation plan:
- Analyze usage patterns
- Purchase reserved instances
- Schedule for renewal
- Track savings
""", modules=["azure", "cost-optimization"])
```

### 3. Lifecycle Policies

```python
# Create lifecycle policies
result = cogos.think("""
Create cost-saving lifecycle policies:
- Disk snapshots
- Storage lifecycle
- ACR image cleanup
- Log Analytics retention
""", modules=["azure", "storage", "acr"])
```

---

## Security

### 1. Network Security

```python
# Secure network configuration
result = cogos.think("""
Create secure network setup:
- VNet with private clusters
- Network security groups
- Application Gateway WAF
- Azure Firewall
- Private endpoints
- Azure DDoS Protection
""", modules=["azure", "security", "vnet"])
```

### 2. Secrets Management

```python
# Implement secrets management
result = cogos.think("""
Implement secrets management:
- Azure Key Vault
- Azure AD Workload Identity
- CSI Secret Store
- Encrypted environment variables
- Rotation policies
""", modules=["azure", "key-vault", "kubernetes"])
```

### 3. Compliance

```python
# Create compliance setup
result = cogos.think("""
Implement Azure compliance features:
- Azure Policy
- Azure Blueprints
- Azure Security Center
- Azure Defender
- Compliance Manager
""", modules=["azure", "compliance", "security"])
```

---

## Disaster Recovery

### 1. Backup Strategy

```python
# Create backup strategy
result = cogos.think("""
Create comprehensive backup strategy:
- Azure SQL backups
- Azure SQL long-term retention
- Disk snapshots
- Azure Backup
- Geo-redundant storage
""", modules=["azure", "azure-sql", "backup"])
```

### 2. Multi-Region Setup

```python
# Create multi-region deployment
result = cogos.think("""
Design multi-region architecture:
- Multi-region clusters
- Traffic Manager
- Database replication
- Data synchronization
- Failover procedures
- Health probes
""", modules=["azure", "traffic-manager", "azure-sql", "kubernetes"])
```

---

## Example: Complete AKS Deployment

```python
# Deploy complete application to AKS
cogos = CogOS()

# 1. Create infrastructure
infrastructure = cogos.think("""
Create Azure infrastructure for AKS:
- Resource group
- VNet (10.0.0.0/16)
- 3 subnets
- AKS cluster (1.28+)
- Azure SQL Database
- Azure Cache for Redis
- Application Gateway
- Azure Container Registry
- Key Vault
""", modules=["azure", "aks", "terraform"])

# 2. Build and push Docker image
docker = cogos.think("""
Create Docker setup:
- Multi-stage Dockerfile
- Build and test image
- Tag for ACR
- Push to Azure Container Registry
""", modules=["docker", "azure"], context=infrastructure)

# 3. Deploy to AKS
deployment = cogos.think("""
Deploy to AKS:
- Namespace
- Deployment (3 replicas)
- Service (LoadBalancer)
- Ingress (Application Gateway + SSL)
- ConfigMap (environment)
- Secret (from Key Vault)
- HPA (min 3, max 10)
""", modules=["kubernetes", "azure", "helm"], context=infrastructure)

# 4. Set up monitoring
monitoring = cogos.think("""
Deploy monitoring stack:
- Azure Monitor
- Container insights
- Application Insights
- Dashboards
- Alert rules
- Action groups
""", modules=["azure", "monitoring"], context=infrastructure)

# 5. Set up CI/CD
cicd = cogos.think("""
Create Azure DevOps pipeline:
- Build Docker image
- Run tests
- Push to ACR
- Deploy to AKS
- Run smoke tests
- Notify on failure
""", modules=["azure", "azure-devops", "docker", "kubernetes"], context=infrastructure)
```

---

## Best Practices

1. **Use Infrastructure as Code** - Terraform or Bicep
2. **Use Azure AD** - Enable Azure AD integration
3. **Enable monitoring** - Azure Monitor, Application Insights
4. **Set up alerts** - Action groups, alert rules
5. **Use tags** - Tag all Azure resources
6. **Enable logging** - Diagnostic logs, Activity logs
7. **Secure secrets** - Key Vault, not plain text
8. **Auto-scaling** - HPA, Cluster autoscaler
9. **Cost optimization** - Use spot, right-size VMs
10. **Disaster recovery** - Backups, multi-region

---

## Troubleshooting

### Cluster Issues

```bash
# Check cluster status
az aks list
az aks show --resource-group RG_NAME --name CLUSTER_NAME

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

- [AKS Documentation](https://docs.microsoft.com/azure/aks/)
- [Azure Best Practices](https://docs.microsoft.com/azure/architecture/best-practices)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)

---

**Back to:** [DevOps Examples](devops.md)
