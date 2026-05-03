# Web Development Examples

Examples of using CogOS for web development projects.

## Table of Contents

- [Frontend Development](#frontend-development)
- [Backend Development](#backend-development)
- [Full-Stack Applications](#full-stack-applications)
- [API Development](#api-development)

---

## Frontend Development

### React Application

```python
from cogos import CogOS

cogos = CogOS()

# Create React component
result = cogos.think("""
Create a React TypeScript component for a user profile card with:
- Avatar image
- User name and email
- Edit button
- Follow/Following toggle
- Responsive design
""")

print(result.code)  # Component code
print(result.tests)  # Jest tests
print(result.styles)  # CSS modules
```

**Output includes:**
- TypeScript component
- Props interface
- State management
- Event handlers
- Jest tests
- CSS modules
- Responsive styles

### Vue.js Application

```python
# Create Vue 3 composition API component
result = cogos.think("""
Create a Vue 3 Composition API component for a data table with:
- Sorting
- Filtering
- Pagination
- Row selection
- Export to CSV
""", modules=["javascript", "vue"])
```

### Next.js Application

```python
# Create Next.js page with SSR
result = cogos.think("""
Create a Next.js 14 page with:
- Server-side rendering
- Static generation
- API routes
- Authentication
- SEO optimization
""", modules=["javascript", "react", "nextjs"])
```

---

## Backend Development

### Express.js API

```python
# Create Express REST API
result = cogos.think("""
Create an Express.js REST API with:
- User authentication (JWT)
- CRUD operations
- Input validation
- Error handling
- Rate limiting
- CORS setup
""", modules=["javascript", "nodejs", "express"])

# Deploy to production
result = cogos.think("""
Deploy the Express API to:
- AWS ECS with Docker
- Auto-scaling
- Load balancer
- CDN integration
""", modules=["nodejs", "aws", "docker"])
```

**Output includes:**
- Express server setup
- Route handlers
- Middleware setup
- Authentication logic
- Docker configuration
- Kubernetes manifests
- CI/CD pipeline

### FastAPI Application

```python
# Create FastAPI application
result = cogos.think("""
Create a FastAPI application with:
- PostgreSQL database
- Redis caching
- WebSocket support
- Background tasks
- API documentation
- Unit tests
""", modules=["python", "fastapi", "postgresql", "redis"])

print(result.code)  # FastAPI app
print(result.tests)  # Pytest tests
print(result.docker)  # Dockerfile
print(result.k8s)  # Kubernetes manifests
```

### Django Application

```python
# Create Django project
result = cogos.think("""
Create a Django e-commerce site with:
- Product catalog
- Shopping cart
- Checkout process
- Payment integration (Stripe)
- Admin panel
- User authentication
""", modules=["python", "django", "postgresql"])
```

---

## Full-Stack Applications

### MERN Stack App

```python
# Create MERN stack application
result = cogos.think("""
Create a MERN stack task management app with:
- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: MongoDB
- Authentication: JWT
- Real-time: Socket.io
- Deployment: Docker + Kubernetes
""", modules=["javascript", "react", "nodejs", "express", "mongodb"])

# Output includes:
# - React frontend
# - Express backend
# - MongoDB schema
# - Socket.io integration
# - Docker compose
# - Kubernetes deployment
```

### Python Full-Stack

```python
# Create Python full-stack app
result = cogos.think("""
Create a real-time chat application with:
- Frontend: React
- Backend: FastAPI
- Database: PostgreSQL + Redis
- WebSocket: FastAPI WebSocket
- Deployment: Docker + AWS
""", modules=["python", "fastapi", "postgresql", "redis", "react", "aws"])
```

---

## API Development

### REST API

```python
# Create REST API
result = cogos.think("""
Create a RESTful API for a blog platform with:
- Posts CRUD
- Comments CRUD
- User management
- Authentication
- Authorization
- Rate limiting
- Pagination
- Filtering
""")

# API documentation
result = cogos.think("""
Generate OpenAPI 3.0 specification for the blog API
""", context=result)
```

### GraphQL API

```python
# Create GraphQL API
result = cogos.think("""
Create a GraphQL API for an e-commerce platform with:
- Product type
- User type
- Order type
- Queries
- Mutations
- Subscriptions
- Authentication
- Authorization
""", modules=["javascript", "graphql", "postgresql"])

print(result.schema)  # GraphQL schema
print(result.resolvers)  # Resolvers
print(result.tests)  # Tests
```

### gRPC Service

```python
# Create gRPC service
result = cogos.think("""
Create a gRPC service for a microservice with:
- Protocol buffer definitions
- Service implementation
- Server setup
- Client examples
- Error handling
- Authentication
""", modules=["python", "grpc"])
```

---

## Web Examples

### 1. Todo App

```python
# Create full todo app
result = cogos.think("""
Create a todo application with:
- React frontend
- FastAPI backend
- PostgreSQL database
- CRUD operations
- User authentication
- Real-time updates
""")

# Deploy it
deployment = cogos.think("""
Deploy the todo app to:
- AWS ECS
- RDS PostgreSQL
- ElastiCache Redis
- Application Load Balancer
""", context=result)
```

### 2. Blog Platform

```python
# Create blog platform
result = cogos.think("""
Create a blog platform with:
- Next.js frontend
- Node.js backend
- MongoDB database
- Markdown support
- Syntax highlighting
- SEO optimization
- RSS feeds
""")

# Add monitoring
monitoring = cogos.think("""
Add monitoring to the blog:
- Google Analytics
- Error tracking (Sentry)
- Performance monitoring
- Uptime monitoring
""", context=result)
```

### 3. E-commerce Site

```python
# Create e-commerce site
result = cogos.think("""
Create an e-commerce site with:
- Product catalog
- Shopping cart
- Checkout process
- Payment integration
- Inventory management
- Order tracking
- Admin dashboard
""")

# Add features
features = cogos.think("""
Add to the e-commerce site:
- Product recommendations
- User reviews
- Wishlist
- Email notifications
- Discount codes
""", context=result)
```

---

## Best Practices

### 1. Component Design

```python
# Design reusable components
result = cogos.think("""
Create a reusable button component with:
- Multiple variants (primary, secondary, danger)
- Sizes (small, medium, large)
- Loading state
- Disabled state
- Icon support
- Accessibility
""", modules=["javascript", "react"])
```

### 2. API Design

```python
# Design RESTful API
result = cogos.think("""
Design a RESTful API following best practices:
- Resource naming
- HTTP methods
- Status codes
- Error handling
- Versioning
- Pagination
- Filtering
- HATEOAS
""", modules=["nodejs", "express"])
```

### 3. Database Design

```python
# Design database schema
result = cogos.think("""
Design a PostgreSQL schema for a social media app with:
- Users table
- Posts table
- Comments table
- Likes table
- Follows table
- Proper indexes
- Foreign keys
- Constraints
""", modules=["postgresql"])
```

---

## Deployment Examples

### Docker Deployment

```python
# Create Docker setup
result = cogos.think("""
Create Docker setup for a Node.js app with:
- Multi-stage Dockerfile
- Docker Compose
- Environment variables
- Volume mounts
- Network configuration
- Health checks
""", modules=["nodejs", "docker"])
```

### Kubernetes Deployment

```python
# Create Kubernetes manifests
result = cogos.think("""
Create Kubernetes deployment for a Python app with:
- Deployment
- Service
- Ingress
- ConfigMap
- Secret
- HPA (Horizontal Pod Autoscaler)
- Pod Disruption Budget
""", modules=["python", "kubernetes"])
```

### AWS Deployment

```python
# Deploy to AWS
result = cogos.think("""
Deploy a web app to AWS with:
- EC2 or ECS
- RDS database
- ElastiCache
- Load balancer
- Auto-scaling
- CloudFront CDN
- Route 53 DNS
""", modules=["aws"])
```

---

## Related Documentation

- [Data Science Examples](data_science.md)
- [DevOps Examples](devops.md)
- [Module API](../api/modules.md)

---

**Next:** [Data Science Examples](data_science.md)
