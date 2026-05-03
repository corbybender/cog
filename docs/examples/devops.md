# DevOps Examples

Examples of using CogOS for DevOps, infrastructure, and operations.

## Table of Contents

- [Infrastructure as Code](#infrastructure-as-code)
- [CI/CD Pipelines](#cicd-pipelines)
- [Container Orchestration](#container-orchestration)
- [Monitoring & Logging](#monitoring--logging)

---

## Infrastructure as Code

### Terraform Configuration

```python
from cogos import CogOS

cogos = CogOS()

# Create AWS infrastructure
result = cogos.think("""
Create Terraform configuration for:
- VPC with public/private subnets
- EC2 instances
- RDS PostgreSQL
- ElastiCache Redis
- Application Load Balancer
- Security groups
- S3 buckets
""", modules=["aws", "terraform"])

print(result.terraform)  # Terraform files
print(result.variables)  # Variables definition
print(result.outputs)  # Outputs
```

### Kubernetes manifests

```python
# Create Kubernetes resources
result = cogos.think("""
Create Kubernetes manifests for a web application:
- Deployment
- Service
- Ingress
- ConfigMap
- Secret
- HPA
- PodDisruptionBudget
- NetworkPolicy
""", modules=["kubernetes", "helm"])

print(result.manifests)  # YAML manifests
print(result.helm_chart)  # Helm chart
print(result.values)  # Values file
```

### Docker Configuration

```python
# Create Docker setup
result = cogos.think("""
Create Docker configuration for a Python app:
- Multi-stage Dockerfile
- Docker Compose
- Environment configuration
- Volume mounts
- Network setup
- Health checks
""", modules=["python", "docker"])

print(result.dockerfile)  # Dockerfile
print(result.compose)  # docker-compose.yml
```

---

## CI/CD Pipelines

### GitHub Actions

```python
# Create GitHub Actions workflow
result = cogos.think("""
Create GitHub Actions workflow for:
- Linting and formatting
- Running tests
- Building Docker image
- Pushing to registry
- Deploying to Kubernetes
- Running smoke tests
- Notifying on failure
""", modules=["github", "docker", "kubernetes"])

print(result.workflow)  # YAML workflow
print(result.jobs)  # Job definitions
```

### GitLab CI

```python
# Create GitLab CI pipeline
result = cogos.think("""
Create GitLab CI pipeline for:
- Build stage
- Test stage
- Deploy stage
- Production stage
- Manual approvals
- Environment variables
- Artifacts
""", modules=["gitlab", "docker", "kubernetes"])
```

### Jenkins Pipeline

```python
# Create Jenkins pipeline
result = cogos.think("""
Create Jenkins Declarative Pipeline for:
- Checkout code
- Run tests
- Build application
- Docker build
- Deploy to staging
- Run integration tests
- Deploy to production
""", modules=["jenkins", "docker", "kubernetes"])
```

---

## Container Orchestration

### Kubernetes Deployment

```python
# Deploy to Kubernetes
result = cogos.think("""
Create complete Kubernetes deployment:
- Namespace
- Deployment with replicas
- Service (ClusterIP)
- Ingress with TLS
- ConfigMap for config
- Secret for credentials
- HPA for scaling
- PodDisruptionBudget
- ServiceMonitor for monitoring
""", modules=["kubernetes", "prometheus"])

# Deploy the manifests
deploy = cogos.think("""
Deploy the Kubernetes manifests:
- kubectl apply commands
- Wait for rollout
- Verify deployment
- Run smoke tests
""", context=result)
```

### Helm Chart

```python
# Create Helm chart
result = cogos.think("""
Create Helm chart for microservice:
- Chart.yaml
- Values.yaml
- Templates for all resources
- NOTES.txt for post-install instructions
- Helpers template functions
- Dependency management
""", modules=["kubernetes", "helm"])

print(result.chart)  # Complete Helm chart
print(result.install)  # Installation instructions
```

### Docker Swarm

```python
# Create Docker Swarm setup
result = cogos.think("""
Create Docker Swarm deployment:
- Docker Compose for Swarm
- Secrets management
- Configs
- Services with replicas
- Networks
- Rolling updates
""", modules=["docker", "swarm"])
```

---

## Monitoring & Logging

### Prometheus Setup

```python
# Create Prometheus monitoring
result = cogos.think("""
Set up Prometheus monitoring for:
- Service discovery
- Metrics scraping
- Alerting rules
- Recording rules
- Grafana dashboards
- Alertmanager
""", modules=["prometheus", "grafana", "kubernetes"])

print(result.prometheus)  # Prometheus config
print(result.grafana)  # Grafana dashboards
print(result.alerts)  # Alert rules
```

### ELK Stack

```python
# Create ELK stack setup
result = cogos.think("""
Deploy ELK stack for logging:
- Elasticsearch cluster
- Logstash pipelines
- Kibana dashboards
- Filebeat on nodes
- Metricbeat for metrics
- Index templates
""", modules=["elasticsearch", "kibana", "logstash", "docker"])
```

### Distributed Tracing

```python
# Set up distributed tracing
result = cogos.think("""
Implement distributed tracing with Jaeger:
- Instrumentation
- Span propagation
- Sampling strategy
- Storage backend
- UI configuration
""", modules=["jaeger", "kubernetes", "python"])
```

---

## Complete Examples

### 1. Microservice Infrastructure

```python
# Create complete microservice infrastructure
result = cogos.think("""
Create infrastructure for microservices:
- AWS VPC configuration
- EKS cluster
- RDS databases
- ElastiCache
- Application Load Balancer
- Route53 DNS
- CloudFront CDN
- S3 buckets
- Security groups
- IAM roles
""", modules=["aws", "kubernetes", "terraform"])

# Add CI/CD
cicd = cogos.think("""
Add CI/CD pipeline:
- GitHub Actions workflow
- Build and test
- Docker image build
- Push to ECR
- Deploy to EKS
- Smoke tests
- Rollback on failure
""", context=result)

# Add monitoring
monitoring = cogos.think("""
Add monitoring stack:
- Prometheus
- Grafana
- Alertmanager
- Custom dashboards
- Alert rules
""", context=result)
```

### 2. Serverless Application

```python
# Create serverless application
result = cogos.think("""
Create serverless API on AWS:
- API Gateway
- Lambda functions
- DynamoDB tables
- S3 buckets
- Cognito for auth
- CloudFront distribution
- Route53 custom domain
""", modules=["aws", "lambda", "api-gateway"])

# Add CI/CD
cicd = cogos.think("""
Add CI/CD for serverless:
- SAM template
- GitHub Actions
- Automated deployment
- Stage promotions
""", context=result)
```

### 3. Multi-Region Deployment

```python
# Create multi-region setup
result = cogos.think("""
Design multi-region deployment:
- Active-active regions
- DNS routing (Route53)
- Database replication
- Data synchronization
- Disaster recovery
- Failover procedures
""", modules=["aws", "kubernetes", "postgresql"])
```

---

## Automation Scripts

### Deployment Script

```python
# Create deployment script
result = cogos.think("""
Create deployment script that:
- Checks prerequisites
- Builds Docker image
- Runs tests
- Deploys to Kubernetes
- Waits for rollout
- Runs smoke tests
- Sends notification
""", modules=["bash", "docker", "kubernetes"])
```

### Backup Script

```python
# Create backup script
result = cogos.think("""
Create backup script for:
- Database dumps
- File backups
- Snapshot EBS volumes
- Upload to S3
- Retention policy
- Backup verification
- Notification on failure
""", modules=["bash", "aws", "postgresql"])
```

### Monitoring Script

```python
# Create monitoring script
result = cogos.think("""
Create monitoring script that:
- Checks service health
- Tests endpoints
- Checks resource usage
- Sends alerts
- Logs metrics
- Generates reports
""", modules=["bash", "prometheus", "python"])
```

---

## Security

### Security Hardening

```python
# Create security hardening guide
result = cogos.think("""
Create security hardening for:
- Kubernetes pods
- Network policies
- RBAC configuration
- Secrets management
- Image scanning
- Admission controllers
""", modules=["kubernetes", "security"])
```

### Compliance

```python
# Create compliance checklist
result = cogos.think("""
Create compliance checklist for:
- GDPR compliance
- SOC 2 requirements
- HIPAA requirements
- Security audits
- Penetration testing
""", modules=["security", "compliance"])
```

---

## Related Documentation

- [Web Examples](web.md)
- [Data Science Examples](data_science.md)
- [Module API](../api/modules.md)

---

**Next:** [Deployment Guides](deployment_aws.md)
