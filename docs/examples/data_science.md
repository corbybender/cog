# Data Science Examples

Examples of using CogOS for data science and machine learning projects.

## Table of Contents

- [Data Analysis](#data-analysis)
- [Machine Learning](#machine-learning)
- [Data Engineering](#data-engineering)
- [Visualization](#visualization)

---

## Data Analysis

### Pandas Analysis

```python
from cogos import CogOS

cogos = CogOS()

# Analyze dataset
result = cogos.think("""
Analyze a sales dataset with pandas:
- Load CSV file
- Clean missing values
- Calculate statistics
- Find trends
- Detect outliers
- Generate insights
""", modules=["python"])

print(result.code)  # Analysis code
print(result.explanation)  # Insights
```

**Output includes:**
- Data loading code
- Cleaning functions
- Statistical analysis
- Visualization code
- Insights and recommendations

### Exploratory Data Analysis

```python
# Perform EDA
result = cogos.think("""
Perform exploratory data analysis on customer data:
- Summary statistics
- Distribution plots
- Correlation analysis
- Feature relationships
- Missing data patterns
- Outlier detection
""", modules=["python", "matplotlib", "seaborn"])
```

### Time Series Analysis

```python
# Analyze time series
result = cogos.think("""
Analyze stock price time series:
- Load and preprocess data
- Calculate moving averages
- Detect trends
- Seasonal decomposition
- Forecast with ARIMA
- Visualize results
""", modules=["python", "statsmodels"])
```

---

## Machine Learning

### Classification Model

```python
# Create classification pipeline
result = cogos.think("""
Build a customer churn prediction model:
- Data preprocessing
- Feature engineering
- Train/test split
- Model training (Random Forest)
- Hyperparameter tuning
- Evaluation metrics
- Feature importance
- Export model
""", modules=["python", "scikit-learn"])

print(result.pipeline)  # ML pipeline
print(result.model)  # Trained model
print(result.evaluation)  # Metrics
```

### Regression Model

```python
# Build regression model
result = cogos.think("""
Build a house price prediction model:
- Feature selection
- Linear regression
- Polynomial features
- Regularization (Ridge/Lasso)
- Cross-validation
- Residual analysis
- Prediction intervals
""", modules=["python", "scikit-learn"])
```

### Deep Learning

```python
# Create neural network
result = cogos.think("""
Build an image classification CNN:
- Data augmentation
- CNN architecture
- Transfer learning (ResNet)
- Training loop
- Validation
- Early stopping
- Model checkpointing
- Evaluation
""", modules=["python", "tensorflow", "keras"])
```

### NLP Pipeline

```python
# Build NLP pipeline
result = cogos.think("""
Create a sentiment analysis pipeline:
- Text preprocessing
- Tokenization
- Word embeddings
- LSTM/Transformer model
- Training
- Evaluation
- Inference function
""", modules=["python", "tensorflow", "nlp"])
```

---

## Data Engineering

### ETL Pipeline

```python
# Create ETL pipeline
result = cogos.think("""
Build an ETL pipeline:
- Extract from API
- Transform data
- Load to PostgreSQL
- Error handling
- Logging
- Scheduling
- Monitoring
""", modules=["python", "postgresql", "airflow"])

print(result.pipeline)  # DAG definition
print(result.tasks)  # Task definitions
print(result.tests)  # Unit tests
```

### Data Warehouse

```python
# Design data warehouse
result = cogos.think("""
Design a data warehouse schema:
- Dimension tables
- Fact tables
- Star schema
- SCD type 2
- Partitioning
- Indexes
- ETL processes
""", modules=["postgresql", "data-modeling"])
```

### Real-time Pipeline

```python
# Create streaming pipeline
result = cogos.think("""
Build a real-time data pipeline:
- Kafka producer
- Stream processing
- Windowing operations
- Aggregations
- Sink to database
- Monitoring
""", modules=["python", "kafka", "spark"])
```

---

## Visualization

### Interactive Dashboard

```python
# Create Plotly dashboard
result = cogos.think("""
Create an interactive sales dashboard:
- Line charts (trends)
- Bar charts (comparisons)
- Heatmaps (correlations)
- Filters and controls
- Responsive design
- Export functionality
""", modules=["python", "plotly", "dash"])
```

### Statistical Plots

```python
# Create statistical visualizations
result = cogos.think("""
Create statistical plots for A/B test results:
- Histograms
- Box plots
- Confidence intervals
- P-value visualization
- Effect size plots
- Power analysis
""", modules=["python", "matplotlib", "seaborn", "scipy"])
```

### Geographic Visualization

```python
# Create map visualizations
result = cogos.think("""
Create geographic data visualizations:
- Choropleth maps
- Point maps
- Heat maps
- Cluster maps
- Interactive layers
""", modules=["python", "folium", "geopandas"])
```

---

## Complete Examples

### 1. Customer Segmentation

```python
# End-to-end segmentation project
result = cogos.think("""
Build a customer segmentation system:
- Data collection
- Cleaning and preprocessing
- Feature engineering
- K-means clustering
- Segment analysis
- Visualization
- Deployment (FastAPI)
""", modules=["python", "scikit-learn", "fastapi", "matplotlib"])

# Deploy to production
deployment = cogos.think("""
Deploy the segmentation system:
- Docker containerization
- Kubernetes deployment
- API documentation
- Monitoring setup
""", context=result)
```

### 2. Fraud Detection

```python
# Build fraud detection system
result = cogos.think("""
Create a fraud detection system:
- Imbalanced data handling
- Feature engineering
- Anomaly detection
- Model training (XGBoost)
- Real-time scoring
- Alert system
""", modules=["python", "xgboost", "fastapi", "redis"])

# Add monitoring
monitoring = cogos.think("""
Add monitoring to fraud detection:
- Performance metrics
- Drift detection
- Alerting
- Retraining pipeline
""", context=result)
```

### 3. Recommendation System

```python
# Build recommendation engine
result = cogos.think("""
Build a product recommendation system:
- Collaborative filtering
- Content-based filtering
- Hybrid approach
- Matrix factorization
- Real-time recommendations
- A/B testing
""", modules=["python", "scikit-learn", "redis", "fastapi"])
```

### 4. Time Series Forecasting

```python
# Build forecasting system
result = cogos.think("""
Create a demand forecasting system:
- Data preprocessing
- Feature engineering
- Multiple models (ARIMA, Prophet, LSTM)
- Ensemble
- Evaluation
- Deployment
- Monitoring
""", modules=["python", "statsmodels", "prophet", "tensorflow"])
```

---

## Best Practices

### 1. Data Validation

```python
# Add data validation
result = cogos.think("""
Create data validation pipeline:
- Schema validation
- Type checking
- Range validation
- Null checks
- Duplicate detection
- Data quality reports
""", modules=["python", "great-expectations"])
```

### 2. Model Monitoring

```python
# Add model monitoring
result = cogos.think("""
Implement model monitoring:
- Prediction drift
- Data drift
- Performance metrics
- Alerting
- Retraining triggers
""", modules=["python", "mlflow", "prometheus"])
```

### 3. Experiment Tracking

```python
# Set up experiment tracking
result = cogos.think("""
Create ML experiment tracking:
- MLflow integration
- Hyperparameter logging
- Metric tracking
- Model versioning
- Artifact storage
- Comparison UI
""", modules=["python", "mlflow"])
```

---

## Deployment Examples

### Model API

```python
# Deploy model as API
result = cogos.think("""
Create model API with FastAPI:
- Model loading
- Prediction endpoint
- Batch prediction
- Input validation
- Error handling
- Documentation
- Docker support
""", modules=["python", "fastapi", "scikit-learn"])
```

### Batch Inference

```python
# Create batch inference job
result = cogos.think("""
Create batch inference pipeline:
- Data loading
- Batch prediction
- Result storage
- Error handling
- Logging
- Scheduling
""", modules=["python", "airflow", "scikit-learn"])
```

### Model Monitoring Dashboard

```python
# Create monitoring dashboard
result = cogos.think("""
Build model monitoring dashboard:
- Performance metrics
- Drift detection
- Data distributions
- Alert history
- Model comparison
""", modules=["python", "plotly", "dash", "prometheus"])
```

---

## Related Documentation

- [Web Examples](web.md)
- [DevOps Examples](devops.md)
- [Python API](../api/python.md)

---

**Next:** [DevOps Examples](devops.md)
