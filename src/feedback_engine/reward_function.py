
"""
Reward function for RL feedback system.
"""

import numpy as np
from typing import Dict, Any

class RewardFunction:
    def __init__(self):
        self.weights = {
            'fidelity': 0.3,
            'utility': 0.3,
            'privacy': 0.2,
            'bias': 0.2
        }
    
    def calculate_reward(self, validation_scores: Dict[str, Any]) -> float:
        """Calculate reward based on validation scores."""
        reward = 0.0
        
        # Fidelity reward
        if 'fidelity' in validation_scores and 'fidelity_score' in validation_scores['fidelity']:
            fidelity_score = validation_scores['fidelity']['fidelity_score']
            reward += self.weights['fidelity'] * fidelity_score
        
        # Utility reward
        if 'task_utility' in validation_scores and 'utility_score' in validation_scores['task_utility']:
            utility_score = validation_scores['task_utility']['utility_score']
            reward += self.weights['utility'] * utility_score
        
        # Privacy reward (higher privacy = higher reward)
        if 'privacy_risk' in validation_scores and 'privacy_risk_score' in validation_scores['privacy_risk']:
            privacy_score = 1.0 - validation_scores['privacy_risk']['privacy_risk_score']
            reward += self.weights['privacy'] * privacy_score
        
        # Bias reward (lower bias = higher reward)
        if 'bias_check' in validation_scores and 'overall_bias_score' in validation_scores['bias_check']:
            bias_score = 1.0 - min(1.0, validation_scores['bias_check']['overall_bias_score'])
            reward += self.weights['bias'] * bias_score
        
        return np.clip(reward, 0.0, 1.0)
    
    def get_detailed_feedback(self, validation_scores: Dict[str, Any]) -> Dict[str, str]:
        """Provide detailed feedback for generator improvement."""
        feedback = {}
        
        # Fidelity feedback
        if 'fidelity' in validation_scores:
            fidelity_score = validation_scores['fidelity'].get('fidelity_score', 0)
            if fidelity_score < 0.7:
                feedback['fidelity'] = "Improve statistical fidelity - correlation patterns not preserved"
        
        # Privacy feedback
        if 'privacy_risk' in validation_scores:
            privacy_risk = validation_scores['privacy_risk'].get('privacy_risk_score', 0)
            if privacy_risk > 0.5:
                feedback['privacy'] = "High privacy risk detected - add more noise or use differential privacy"
        
        # Bias feedback
        if 'bias_check' in validation_scores:
            bias_score = validation_scores['bias_check'].get('overall_bias_score', 0)
            if bias_score > 0.3:
                feedback['bias'] = "Bias patterns not properly preserved - adjust generation process"
        
        return feedback
