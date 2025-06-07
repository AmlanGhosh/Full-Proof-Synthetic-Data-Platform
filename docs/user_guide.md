
# User Guide

## Getting Started

The Full-Proof Synthetic Data Validation Platform provides comprehensive validation of synthetic datasets across multiple quality dimensions.

## Basic Usage

### 1. API Validation

Send a POST request to the `/validate/` endpoint with your real and synthetic datasets:

```bash
curl -X POST "http://localhost:5000/validate/" \
     -F "real_data=@real_dataset.csv" \
     -F "synthetic_data=@synthetic_dataset.csv"
```

### 2. Custom Configuration

You can customize validation by providing a configuration object:

```python
config = {
    "validators": ["fidelity", "privacy_risk", "bias_check"],
    "target_column": "income",
    "protected_attributes": ["gender", "race"]
}
```

## Validation Dimensions

### Fidelity
Measures how well synthetic data preserves statistical properties of real data.
- **Metrics**: Correlation difference, KS statistic
- **Score Range**: 0-1 (higher is better)

### Task Utility
Evaluates how well synthetic data performs in downstream ML tasks.
- **Metrics**: F1 score comparison using RandomForest
- **Score Range**: 0-1 (higher is better)

### Bias Assessment
Checks if bias patterns from real data are preserved appropriately.
- **Metrics**: Demographic Parity Difference
- **Score Range**: 0-1 (lower bias difference is better)

### Privacy Risk
Assesses privacy risks through membership inference attacks.
- **Metrics**: ROC AUC of membership inference
- **Score Range**: 0-1 (lower risk is better)

### Causal Consistency
Validates preservation of causal relationships.
- **Metrics**: Delta ATE, structural invariance
- **Score Range**: 0-1 (higher consistency is better)

## Interpreting Results

The platform returns a comprehensive validation report including:

1. **Overall Quality Score**: Weighted average of all validation dimensions
2. **Individual Scores**: Detailed results for each validator
3. **Quality Grade**: Human-readable quality assessment
4. **Recommendations**: Specific suggestions for improvement

## Human Review Workflow

When uncertainty is detected (H(v) > threshold), the system routes cases for human review:

1. **Automatic Detection**: Uncertainty detector identifies borderline cases
2. **Context Generation**: Relevant information prepared for reviewers
3. **Review Interface**: Web-based interface for human evaluation
4. **Decision Logging**: All review decisions are audited

## Best Practices

1. **Data Preparation**: Ensure consistent column names and data types
2. **Configuration**: Specify appropriate target and protected attributes
3. **Thresholds**: Adjust uncertainty thresholds based on use case
4. **Monitoring**: Regular audit log review for compliance

## Troubleshooting

### Common Issues

1. **Missing Columns**: Ensure synthetic data has same columns as real data
2. **Data Type Mismatches**: Check that numerical columns are properly formatted
3. **Small Sample Sizes**: Some validators require minimum sample sizes
4. **Memory Issues**: Large datasets may require chunked processing
