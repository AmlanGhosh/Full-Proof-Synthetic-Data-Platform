
"""
Aggregates validation scores into Synthetic Data Quality Score.
"""

import numpy as np
from typing import Dict, Any

class ScoreAggregator:
    def __init__(self):
        self.weights = {
            'fidelity': 0.25,
            'task_utility': 0.25,
            'bias_check': 0.20,
            'privacy_risk': 0.15,
            'causal_consistency': 0.15
        }
    
    def calculate_synthetic_data_quality_score(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall Synthetic Data Quality Score."""
        scores = {}
        weighted_sum = 0.0
        total_weight = 0.0
        
        # Extract individual scores
        for validator_name, results in validation_results.items():
            if validator_name == 'fidelity' and 'fidelity_score' in results:
                scores['fidelity'] = results['fidelity_score']
                weighted_sum += scores['fidelity'] * self.weights['fidelity']
                total_weight += self.weights['fidelity']
            
            elif validator_name == 'task_utility' and 'utility_score' in results:
                scores['task_utility'] = results['utility_score']
                weighted_sum += scores['task_utility'] * self.weights['task_utility']
                total_weight += self.weights['task_utility']
            
            elif validator_name == 'bias_check' and 'overall_bias_score' in results:
                # Convert bias score (lower is better) to quality score (higher is better)
                bias_quality = 1.0 - min(1.0, results['overall_bias_score'])
                scores['bias_check'] = bias_quality
                weighted_sum += bias_quality * self.weights['bias_check']
                total_weight += self.weights['bias_check']
            
            elif validator_name == 'privacy_risk' and 'privacy_risk_score' in results:
                # Convert privacy risk (lower is better) to privacy quality (higher is better)
                privacy_quality = 1.0 - results['privacy_risk_score']
                scores['privacy_risk'] = privacy_quality
                weighted_sum += privacy_quality * self.weights['privacy_risk']
                total_weight += self.weights['privacy_risk']
            
            elif validator_name == 'causal_consistency' and 'causal_consistency_score' in results:
                scores['causal_consistency'] = results['causal_consistency_score']
                weighted_sum += scores['causal_consistency'] * self.weights['causal_consistency']
                total_weight += self.weights['causal_consistency']
        
        # Calculate overall score
        overall_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        return {
            'overall_synthetic_data_quality_score': overall_score,
            'individual_scores': scores,
            'weights_used': {k: v for k, v in self.weights.items() if k in scores},
            'quality_grade': self._get_quality_grade(overall_score)
        }
    
    def _get_quality_grade(self, score: float) -> str:
        """Convert numeric score to quality grade."""
        if score >= 0.9:
            return 'Excellent'
        elif score >= 0.8:
            return 'Good'
        elif score >= 0.7:
            return 'Fair'
        elif score >= 0.6:
            return 'Poor'
        else:
            return 'Very Poor'
