
import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.validator_modules.fidelity import FidelityValidator
from src.validator_modules.privacy_risk import PrivacyRiskValidator
from src.validator_modules.bias_check import BiasValidator
from src.validator_modules.task_utility import TaskUtilityValidator
from src.validator_modules.causal_consistency import CausalConsistencyValidator
from src.orchestrator import ValidationOrchestrator
from src.aggregator import ScoreAggregator

class TestFidelityValidator:
    def setup_method(self):
        self.validator = FidelityValidator()
        # Create sample data
        np.random.seed(42)
        self.real_data = pd.DataFrame({
            'age': np.random.normal(40, 10, 1000),
            'income': np.random.normal(50000, 15000, 1000),
            'score': np.random.uniform(0, 100, 1000)
        })
        self.synthetic_data = pd.DataFrame({
            'age': np.random.normal(42, 12, 1000),
            'income': np.random.normal(52000, 16000, 1000),
            'score': np.random.uniform(0, 100, 1000)
        })
    
    def test_validate_returns_dict(self):
        result = self.validator.validate(self.real_data, self.synthetic_data)
        assert isinstance(result, dict)
        assert 'fidelity_score' in result
        assert 'correlation_difference' in result
        assert 'ks_test_results' in result
    
    def test_fidelity_score_range(self):
        result = self.validator.validate(self.real_data, self.synthetic_data)
        assert 0 <= result['fidelity_score'] <= 1

class TestPrivacyRiskValidator:
    def setup_method(self):
        self.validator = PrivacyRiskValidator()
        np.random.seed(42)
        self.real_data = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 500),
            'feature2': np.random.normal(0, 1, 500),
            'feature3': np.random.normal(0, 1, 500)
        })
        self.synthetic_data = pd.DataFrame({
            'feature1': np.random.normal(0.1, 1.1, 500),
            'feature2': np.random.normal(0.1, 1.1, 500),
            'feature3': np.random.normal(0.1, 1.1, 500)
        })
    
    def test_validate_returns_dict(self):
        result = self.validator.validate(self.real_data, self.synthetic_data)
        assert isinstance(result, dict)
        assert 'privacy_risk_score' in result
        assert 'membership_inference_auc' in result
    
    def test_privacy_risk_score_range(self):
        result = self.validator.validate(self.real_data, self.synthetic_data)
        assert 0 <= result['privacy_risk_score'] <= 1

class TestValidationOrchestrator:
    def setup_method(self):
        self.orchestrator = ValidationOrchestrator()
        np.random.seed(42)
        self.real_data = pd.DataFrame({
            'age': np.random.randint(18, 80, 100),
            'income': np.random.normal(50000, 15000, 100),
            'gender': np.random.choice(['M', 'F'], 100),
            'target': np.random.binomial(1, 0.3, 100)
        })
        self.synthetic_data = pd.DataFrame({
            'age': np.random.randint(18, 80, 100),
            'income': np.random.normal(52000, 16000, 100),
            'gender': np.random.choice(['M', 'F'], 100),
            'target': np.random.binomial(1, 0.35, 100)
        })
    
    def test_fidelity_only_config(self):
        config = {'validators': ['fidelity']}
        result = self.orchestrator.run_validation_pipeline(
            self.real_data, self.synthetic_data, config
        )
        assert 'fidelity' in result
        assert len(result) == 1
    
    def test_multiple_validators_config(self):
        config = {
            'validators': ['fidelity', 'privacy_risk'],
            'target_column': 'target',
            'protected_attributes': ['gender']
        }
        result = self.orchestrator.run_validation_pipeline(
            self.real_data, self.synthetic_data, config
        )
        assert 'fidelity' in result
        assert 'privacy_risk' in result

class TestScoreAggregator:
    def setup_method(self):
        self.aggregator = ScoreAggregator()
    
    def test_calculate_quality_score(self):
        validation_results = {
            'fidelity': {'fidelity_score': 0.8},
            'privacy_risk': {'privacy_risk_score': 0.3}
        }
        result = self.aggregator.calculate_synthetic_data_quality_score(validation_results)
        assert 'overall_synthetic_data_quality_score' in result
        assert 'individual_scores' in result
        assert 'quality_grade' in result
    
    def test_score_range(self):
        validation_results = {
            'fidelity': {'fidelity_score': 0.9},
            'privacy_risk': {'privacy_risk_score': 0.2}
        }
        result = self.aggregator.calculate_synthetic_data_quality_score(validation_results)
        assert 0 <= result['overall_synthetic_data_quality_score'] <= 1
