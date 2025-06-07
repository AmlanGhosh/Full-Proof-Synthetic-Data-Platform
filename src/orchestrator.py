
"""
Validation orchestrator that routes data through validation pipelines.
"""

import pandas as pd
from typing import Dict, Any, List
from .validator_modules.fidelity import FidelityValidator
from .validator_modules.task_utility import TaskUtilityValidator
from .validator_modules.bias_check import BiasValidator
from .validator_modules.privacy_risk import PrivacyRiskValidator
from .validator_modules.causal_consistency import CausalConsistencyValidator

class ValidationOrchestrator:
    def __init__(self):
        self.validators = {
            'fidelity': FidelityValidator(),
            'task_utility': TaskUtilityValidator(),
            'bias_check': BiasValidator(),
            'privacy_risk': PrivacyRiskValidator(),
            'causal_consistency': CausalConsistencyValidator()
        }
    
    def run_validation_pipeline(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame,
                               config: Dict[str, Any]) -> Dict[str, Any]:
        """Run complete validation pipeline."""
        results = {}
        
        # Fidelity validation
        if 'fidelity' in config.get('validators', []):
            results['fidelity'] = self.validators['fidelity'].validate(real_data, synthetic_data)
        
        # Task utility validation
        if 'task_utility' in config.get('validators', []) and 'target_column' in config:
            results['task_utility'] = self.validators['task_utility'].validate(
                real_data, synthetic_data, config['target_column']
            )
        
        # Bias check validation
        if 'bias_check' in config.get('validators', []):
            results['bias_check'] = self.validators['bias_check'].validate(
                real_data, synthetic_data, 
                config.get('protected_attributes', []),
                config.get('target_column', '')
            )
        
        # Privacy risk validation
        if 'privacy_risk' in config.get('validators', []):
            results['privacy_risk'] = self.validators['privacy_risk'].validate(real_data, synthetic_data)
        
        # Causal consistency validation
        if 'causal_consistency' in config.get('validators', []):
            results['causal_consistency'] = self.validators['causal_consistency'].validate(
                real_data, synthetic_data,
                config.get('treatment_column', ''),
                config.get('outcome_column', ''),
                config.get('causal_variables', [])
            )
        
        return results
