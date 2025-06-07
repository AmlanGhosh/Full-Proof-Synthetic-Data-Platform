
"""
Bias check validation module.
Implements bias score calculation and Demographic Parity Difference.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List

class BiasValidator:
    def __init__(self):
        self.name = "Bias Validator"
    
    def demographic_parity_difference(self, data: pd.DataFrame, 
                                    protected_attribute: str, 
                                    target_column: str) -> float:
        """Calculate Demographic Parity Difference."""
        try:
            groups = data[protected_attribute].unique()
            if len(groups) < 2:
                return 0.0
            
            positive_rates = []
            for group in groups:
                group_data = data[data[protected_attribute] == group]
                positive_rate = group_data[target_column].mean()
                positive_rates.append(positive_rate)
            
            # Calculate max difference between groups
            dpd = max(positive_rates) - min(positive_rates)
            return dpd
            
        except Exception as e:
            print(f"Error calculating demographic parity difference: {e}")
            return 1.0  # Worst case bias
    
    def bias_score(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame,
                  protected_attributes: List[str], target_column: str) -> Dict[str, float]:
        """Calculate bias scores for protected attributes."""
        bias_scores = {}
        
        for attr in protected_attributes:
            if attr in real_data.columns and attr in synthetic_data.columns:
                try:
                    dpd_real = self.demographic_parity_difference(real_data, attr, target_column)
                    dpd_synthetic = self.demographic_parity_difference(synthetic_data, attr, target_column)
                    
                    # Bias score: how much synthetic data preserves bias patterns
                    bias_preservation = abs(dpd_real - dpd_synthetic)
                    bias_scores[attr] = bias_preservation
                    
                except Exception as e:
                    print(f"Error calculating bias score for {attr}: {e}")
                    bias_scores[attr] = 1.0
        
        return bias_scores
    
    def validate(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame,
                protected_attributes: List[str], target_column: str) -> Dict[str, Any]:
        """Main validation method for bias checks."""
        bias_scores = self.bias_score(real_data, synthetic_data, protected_attributes, target_column)
        
        # Calculate overall bias score
        overall_bias_score = np.mean(list(bias_scores.values())) if bias_scores else 0.0
        
        return {
            'overall_bias_score': overall_bias_score,
            'attribute_bias_scores': bias_scores,
            'validator_name': self.name
        }
