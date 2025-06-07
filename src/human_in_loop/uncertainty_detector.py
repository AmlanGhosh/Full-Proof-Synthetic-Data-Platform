
"""
Uncertainty detector for routing validation cases to human reviewers.
"""

import numpy as np
from typing import Dict, Any, Tuple

class UncertaintyDetector:
    def __init__(self, uncertainty_threshold: float = 0.3):
        self.uncertainty_threshold = uncertainty_threshold
    
    def calculate_uncertainty(self, validation_results: Dict[str, Any]) -> float:
        """Calculate H(v) - uncertainty score for validation results."""
        uncertainties = []
        
        # Check score variance across validators
        scores = []
        for validator_name, results in validation_results.items():
            if validator_name == 'fidelity' and 'fidelity_score' in results:
                scores.append(results['fidelity_score'])
            elif validator_name == 'task_utility' and 'utility_score' in results:
                scores.append(results['utility_score'])
            elif validator_name == 'privacy_risk' and 'privacy_risk_score' in results:
                scores.append(1.0 - results['privacy_risk_score'])  # Convert to quality score
        
        if len(scores) > 1:
            score_variance = np.var(scores)
            uncertainties.append(score_variance)
        
        # Check for conflicting results
        if len(scores) >= 2:
            max_diff = max(scores) - min(scores)
            uncertainties.append(max_diff)
        
        # Overall uncertainty
        overall_uncertainty = np.mean(uncertainties) if uncertainties else 0.0
        return overall_uncertainty
    
    def should_route_to_human(self, validation_results: Dict[str, Any]) -> Tuple[bool, str]:
        """Determine if validation case should be routed to human reviewer."""
        uncertainty = self.calculate_uncertainty(validation_results)
        
        if uncertainty > self.uncertainty_threshold:
            reason = f"High uncertainty detected (H(v)={uncertainty:.3f})"
            return True, reason
        
        # Check for edge cases
        for validator_name, results in validation_results.items():
            if validator_name == 'privacy_risk':
                privacy_risk = results.get('privacy_risk_score', 0)
                if 0.4 <= privacy_risk <= 0.6:  # Borderline privacy risk
                    return True, "Borderline privacy risk requires human review"
        
        return False, "Automatic validation sufficient"
    
    def generate_human_review_context(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate context information for human reviewers."""
        uncertainty = self.calculate_uncertainty(validation_results)
        should_review, reason = self.should_route_to_human(validation_results)
        
        return {
            'uncertainty_score': uncertainty,
            'requires_human_review': should_review,
            'review_reason': reason,
            'focus_areas': self._identify_focus_areas(validation_results),
            'validation_summary': self._create_summary(validation_results)
        }
    
    def _identify_focus_areas(self, validation_results: Dict[str, Any]) -> list:
        """Identify areas that need human attention."""
        focus_areas = []
        
        for validator_name, results in validation_results.items():
            if validator_name == 'privacy_risk':
                privacy_risk = results.get('privacy_risk_score', 0)
                if privacy_risk > 0.5:
                    focus_areas.append("Privacy risk assessment")
            
            if validator_name == 'bias_check':
                bias_score = results.get('overall_bias_score', 0)
                if bias_score > 0.3:
                    focus_areas.append("Bias preservation analysis")
        
        return focus_areas
    
    def _create_summary(self, validation_results: Dict[str, Any]) -> str:
        """Create a summary of validation results for human reviewers."""
        summary_parts = []
        
        for validator_name, results in validation_results.items():
            if validator_name == 'fidelity':
                score = results.get('fidelity_score', 0)
                summary_parts.append(f"Fidelity: {score:.3f}")
            elif validator_name == 'privacy_risk':
                risk = results.get('privacy_risk_score', 0)
                summary_parts.append(f"Privacy Risk: {risk:.3f}")
        
        return " | ".join(summary_parts)
