
"""
Task utility evaluation module.
Uses RandomForestClassifier and F1 score to evaluate synthetic data utility.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
from typing import Dict, Any, Optional

class TaskUtilityValidator:
    def __init__(self):
        self.name = "Task Utility Validator"
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def evaluate_task_utility(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame, 
                            target_column: str) -> Dict[str, Any]:
        """Evaluate task utility using downstream ML performance."""
        try:
            # Prepare real data
            X_real = real_data.drop(columns=[target_column])
            y_real = real_data[target_column]
            
            # Prepare synthetic data
            X_synthetic = synthetic_data.drop(columns=[target_column])
            y_synthetic = synthetic_data[target_column]
            
            # Train on real data, test on synthetic
            X_train_real, X_test_real, y_train_real, y_test_real = train_test_split(
                X_real, y_real, test_size=0.2, random_state=42
            )
            
            # Train model on real data
            self.model.fit(X_train_real, y_train_real)
            
            # Test on real data (baseline)
            y_pred_real = self.model.predict(X_test_real)
            f1_real = f1_score(y_test_real, y_pred_real, average='weighted')
            
            # Test on synthetic data
            y_pred_synthetic = self.model.predict(X_synthetic)
            f1_synthetic = f1_score(y_synthetic, y_pred_synthetic, average='weighted')
            
            # Calculate utility score (how well synthetic data performs)
            utility_score = f1_synthetic / f1_real if f1_real > 0 else 0
            
            return {
                'utility_score': utility_score,
                'f1_score_real': f1_real,
                'f1_score_synthetic': f1_synthetic,
                'validator_name': self.name
            }
            
        except Exception as e:
            print(f"Error in task utility evaluation: {e}")
            return {
                'utility_score': 0.0,
                'f1_score_real': 0.0,
                'f1_score_synthetic': 0.0,
                'error': str(e),
                'validator_name': self.name
            }
    
    def validate(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame, 
                target_column: str) -> Dict[str, Any]:
        """Main validation method for task utility."""
        return self.evaluate_task_utility(real_data, synthetic_data, target_column)
