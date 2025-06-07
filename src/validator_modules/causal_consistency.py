
"""
Causal consistency validation module.
Implements Delta_ATE and Structural Invariance Test.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

class CausalConsistencyValidator:
    def __init__(self):
        self.name = "Causal Consistency Validator"
    
    def calculate_ate(self, data: pd.DataFrame, treatment_col: str, outcome_col: str) -> float:
        """Calculate Average Treatment Effect (ATE)."""
        try:
            treated = data[data[treatment_col] == 1][outcome_col]
            control = data[data[treatment_col] == 0][outcome_col]
            
            ate = treated.mean() - control.mean()
            return ate
            
        except Exception as e:
            print(f"Error calculating ATE: {e}")
            return 0.0
    
    def delta_ate(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame,
                  treatment_col: str, outcome_col: str) -> float:
        """Calculate difference in ATE between real and synthetic data."""
        try:
            ate_real = self.calculate_ate(real_data, treatment_col, outcome_col)
            ate_synthetic = self.calculate_ate(synthetic_data, treatment_col, outcome_col)
            
            delta_ate = abs(ate_real - ate_synthetic)
            return delta_ate
            
        except Exception as e:
            print(f"Error calculating Delta ATE: {e}")
            return float('inf')
    
    def structural_invariance_test(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame,
                                  variables: list) -> Dict[str, float]:
        """Test structural invariance between real and synthetic data."""
        invariance_scores = {}
        
        for var in variables:
            if var in real_data.columns and var in synthetic_data.columns:
                try:
                    # Simple correlation-based structural test
                    real_corr_with_others = real_data[var].corr(real_data.drop(columns=[var]).mean(axis=1))
                    synthetic_corr_with_others = synthetic_data[var].corr(synthetic_data.drop(columns=[var]).mean(axis=1))
                    
                    invariance_score = abs(real_corr_with_others - synthetic_corr_with_others)
                    invariance_scores[var] = invariance_score
                    
                except Exception as e:
                    print(f"Error in structural invariance test for {var}: {e}")
                    invariance_scores[var] = 1.0
        
        return invariance_scores
    
    def validate(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame,
                treatment_col: str, outcome_col: str, variables: list) -> Dict[str, Any]:
        """Main validation method for causal consistency."""
        delta_ate_score = self.delta_ate(real_data, synthetic_data, treatment_col, outcome_col)
        invariance_scores = self.structural_invariance_test(real_data, synthetic_data, variables)
        
        # Calculate overall causal consistency score
        avg_invariance = np.mean(list(invariance_scores.values())) if invariance_scores else 0.0
        causal_consistency_score = 1.0 / (1.0 + delta_ate_score + avg_invariance)
        
        return {
            'causal_consistency_score': causal_consistency_score,
            'delta_ate': delta_ate_score,
            'structural_invariance_scores': invariance_scores,
            'validator_name': self.name
        }
