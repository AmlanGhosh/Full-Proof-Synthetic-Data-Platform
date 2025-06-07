
# API Reference

## Base URL
```
http://localhost:5000
```

## Endpoints

### POST /validate/

Validate synthetic data against real dataset.

**Parameters:**
- `real_data` (file): CSV file containing real dataset
- `synthetic_data` (file): CSV file containing synthetic dataset  
- `config` (optional, JSON): Validation configuration

**Request Example:**
```bash
curl -X POST "http://localhost:5000/validate/" \
     -F "real_data=@real.csv" \
     -F "synthetic_data=@synthetic.csv" \
     -F 'config={"validators": ["fidelity", "privacy_risk"]}'
```

**Response Schema:**
```json
{
  "status": "success",
  "validation_results": {
    "fidelity": {
      "fidelity_score": 0.85,
      "correlation_difference": 0.12,
      "ks_test_results": {...}
    },
    "privacy_risk": {
      "privacy_risk_score": 0.23,
      "membership_inference_auc": 0.61,
      "privacy_level": "Low"
    }
  },
  "synthetic_data_quality_score": {
    "overall_synthetic_data_quality_score": 0.78,
    "individual_scores": {...},
    "quality_grade": "Good"
  },
  "data_info": {
    "real_data_shape": [1000, 10],
    "synthetic_data_shape": [1000, 10],
    "columns": ["age", "income", "gender"]
  }
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Synthetic Data Validation Platform"
}
```

### GET /

API information endpoint.

**Response:**
```json
{
  "message": "Full-Proof Synthetic Data Validation Platform API"
}
```

## Configuration Options

### Validators
Available validators:
- `fidelity`: Statistical fidelity validation
- `task_utility`: ML task utility evaluation  
- `bias_check`: Bias preservation analysis
- `privacy_risk`: Privacy risk assessment
- `causal_consistency`: Causal relationship validation

### Required Parameters by Validator

**task_utility:**
- `target_column`: Name of target variable column

**bias_check:**
- `target_column`: Name of target variable column
- `protected_attributes`: List of protected attribute column names

**causal_consistency:**
- `treatment_column`: Name of treatment variable column
- `outcome_column`: Name of outcome variable column
- `causal_variables`: List of causal variable column names

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Missing required parameter: target_column"
}
```

### 422 Validation Error
```json
{
  "detail": "Invalid file format. Please upload CSV files."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Validation error: Column 'target' not found in dataset"
}
```

## Rate Limits

- Maximum file size: 100MB per file
- Request timeout: 300 seconds
- Concurrent requests: 10 per client

## Authentication

Currently no authentication required. In production, implement:
- API key authentication
- JWT tokens for user sessions
- Role-based access control
