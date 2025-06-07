<<<<<<< HEAD
# Full-Proof-Synthetic-Data-Platform
This project implements the core validation and feedback mechanisms for a "Full-Proof Synthetic Data Validation and Feedback Platform,".
=======

# Full-Proof Synthetic Data Validation Platform

A comprehensive platform for validating synthetic data quality across multiple dimensions including fidelity, utility, bias, privacy, and causal consistency.

## Features

- **Multi-dimensional Validation**: Comprehensive validation across 5 key dimensions
- **Real-time Processing**: FastAPI-based REST API for real-time validation
- **Human-in-the-Loop**: Uncertainty detection and human review workflows
- **Reinforcement Learning**: Feedback engine for continuous improvement
- **Audit Logging**: Complete audit trails for compliance
- **Explainable Results**: Human-readable validation reports

## Project Structure

```
├── src/                          # Core application code
│   ├── validator_modules/        # Individual validation modules
│   ├── feedback_engine/          # RL-based feedback system
│   ├── human_in_loop/           # Human review components
│   └── explainability_layer/    # Result explanation system
├── data/                        # Datasets and data preparation
├── notebooks/                   # Analysis and experimentation
├── tests/                       # Unit and integration tests
├── docs/                        # Documentation
└── configs/                     # Configuration files
```

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API Server**:
   ```bash
   python -m src.main
   ```

3. **Validate Synthetic Data**:
   ```bash
   curl -X POST "http://localhost:5000/validate/" \
        -F "real_data=@path/to/real_data.csv" \
        -F "synthetic_data=@path/to/synthetic_data.csv"
   ```

## Validation Modules

### 1. Fidelity Validator
- Correlation difference analysis
- Kolmogorov-Smirnov statistical tests
- Distribution similarity metrics

### 2. Task Utility Validator
- Downstream ML performance evaluation
- F1 score comparison
- RandomForest-based utility assessment

### 3. Bias Validator
- Demographic Parity Difference
- Bias preservation analysis
- Protected attribute evaluation

### 4. Privacy Risk Validator
- Membership inference attacks
- ROC AUC privacy risk assessment
- Privacy level classification

### 5. Causal Consistency Validator
- Average Treatment Effect (ATE) analysis
- Structural invariance testing
- Causal relationship preservation

## API Endpoints

- `POST /validate/` - Main validation endpoint
- `GET /health` - Health check endpoint
- `GET /` - API information

## Configuration

Validation can be configured using the following parameters:

```json
{
  "validators": ["fidelity", "task_utility", "bias_check", "privacy_risk", "causal_consistency"],
  "target_column": "target",
  "protected_attributes": ["gender", "race"],
  "treatment_column": "treatment",
  "outcome_column": "outcome",
  "causal_variables": ["age", "income"]
}
```

## Development

1. **Run Tests**:
   ```bash
   python -m pytest tests/
   ```

2. **Generate Documentation**:
   ```bash
   cd docs && make html
   ```

## License

MIT License - see LICENSE file for details.

## Contributing

Please read CONTRIBUTING.md for guidelines on contributing to this project.
>>>>>>> 68f0a37 (Assistant checkpoint: Created complete Full-Proof Synthetic Data Validation Platform structure)
