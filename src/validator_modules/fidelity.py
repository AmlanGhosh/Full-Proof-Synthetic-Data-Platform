
"""
Fidelity validation module.
Implements correlation difference and Kolmogorov-Smirnov statistical tests.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any

class FidelityValidator:
    def __init__(self):
        self.name = "Fidelity Validator"
    
    def correlation_diff(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame) -> float:
        """Calculate correlation difference between real and synthetic data."""
        try:
            real_corr = real_data.corr()
            synthetic_corr = synthetic_data.corr()
            
            # Calculate Frobenius norm of difference
            diff = real_corr - synthetic_corr
            correlation_diff_score = np.linalg.norm(diff, 'fro')
            
            return correlation_diff_score
        except Exception as e:
            print(f"Error calculating correlation difference: {e}")
            return float('inf')
    
    def ks_statistic(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame) -> Dict[str, float]:
        """Perform Kolmogorov-Smirnov test for each numerical column."""
        ks_results = {}
        
        for column in real_data.select_dtypes(include=[np.number]).columns:
            if column in synthetic_data.columns:
                try:
                    ks_stat, p_value = stats.ks_2samp(
                        real_data[column].dropna(), 
                        synthetic_data[column].dropna()
                    )
                    ks_results[column] = {
                        'ks_statistic': ks_stat,
                        'p_value': p_value
                    }
                except Exception as e:
                    print(f"Error in KS test for column {column}: {e}")
                    ks_results[column] = {'ks_statistic': 1.0, 'p_value': 0.0}
        
        return ks_results
    
    def validate(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame) -> Dict[str, Any]:
        """Main validation method for fidelity checks."""
        corr_diff = self.correlation_diff(real_data, synthetic_data)
        ks_results = self.ks_statistic(real_data, synthetic_data)
        
        # Calculate overall fidelity score (lower is better)
        avg_ks = np.mean([result['ks_statistic'] for result in ks_results.values()])
        fidelity_score = 1.0 / (1.0 + corr_diff + avg_ks)  # Normalize to 0-1
        
        return {
            'fidelity_score': fidelity_score,
            'correlation_difference': corr_diff,
            'ks_test_results': ks_results,
            'validator_name': self.name
        }
