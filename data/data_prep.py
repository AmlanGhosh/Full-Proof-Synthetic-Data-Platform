
"""
Script for generating synthetic variants with controlled flaws for testing.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

class DataPreparator:
    def __init__(self):
        self.noise_levels = [0.1, 0.2, 0.3]
    
    def add_noise(self, data: pd.DataFrame, noise_level: float = 0.1) -> pd.DataFrame:
        """Add controlled noise to numerical columns."""
        noisy_data = data.copy()
        
        for col in data.select_dtypes(include=[np.number]).columns:
            noise = np.random.normal(0, noise_level * data[col].std(), size=len(data))
            noisy_data[col] = data[col] + noise
        
        return noisy_data
    
    def introduce_bias(self, data: pd.DataFrame, protected_attr: str, 
                      bias_factor: float = 0.2) -> pd.DataFrame:
        """Introduce controlled bias for testing bias detection."""
        biased_data = data.copy()
        
        if protected_attr in data.columns:
            # Introduce bias by modifying target variable based on protected attribute
            protected_groups = data[protected_attr].unique()
            if len(protected_groups) >= 2:
                # Favor one group over another
                group_to_bias = protected_groups[0]
                mask = biased_data[protected_attr] == group_to_bias
                
                # Modify outcomes for this group
                if 'target' in biased_data.columns:
                    biased_data.loc[mask, 'target'] *= (1 + bias_factor)
        
        return biased_data
    
    def corrupt_correlations(self, data: pd.DataFrame, 
                           corruption_factor: float = 0.3) -> pd.DataFrame:
        """Corrupt correlations between variables."""
        corrupted_data = data.copy()
        
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) >= 2:
            # Randomly shuffle some rows to break correlations
            n_rows_to_shuffle = int(len(data) * corruption_factor)
            rows_to_shuffle = np.random.choice(len(data), n_rows_to_shuffle, replace=False)
            
            col_to_shuffle = np.random.choice(numerical_cols)
            shuffled_values = corrupted_data.loc[rows_to_shuffle, col_to_shuffle].sample(n=n_rows_to_shuffle).values
            corrupted_data.loc[rows_to_shuffle, col_to_shuffle] = shuffled_values
        
        return corrupted_data
    
    def generate_test_variants(self, original_data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Generate multiple test variants with different controlled flaws."""
        variants = {}
        
        # High fidelity variant (minimal changes)
        variants['high_fidelity'] = self.add_noise(original_data, 0.05)
        
        # Medium fidelity variant
        variants['medium_fidelity'] = self.add_noise(original_data, 0.15)
        
        # Low fidelity variant
        variants['low_fidelity'] = self.corrupt_correlations(original_data, 0.4)
        
        # Biased variant
        if 'gender' in original_data.columns or 'race' in original_data.columns:
            protected_attr = 'gender' if 'gender' in original_data.columns else 'race'
            variants['biased'] = self.introduce_bias(original_data, protected_attr, 0.3)
        
        # High privacy risk variant (essentially original data with minimal changes)
        variants['high_privacy_risk'] = original_data.copy()
        
        return variants

if __name__ == "__main__":
    # Example usage
    prep = DataPreparator()
    
    # Generate sample data for testing
    sample_data = pd.DataFrame({
        'age': np.random.randint(18, 80, 1000),
        'income': np.random.normal(50000, 15000, 1000),
        'gender': np.random.choice(['M', 'F'], 1000),
        'target': np.random.binomial(1, 0.3, 1000)
    })
    
    variants = prep.generate_test_variants(sample_data)
    
    # Save variants
    for variant_name, variant_data in variants.items():
        variant_data.to_csv(f"synthetic_variants/{variant_name}.csv", index=False)
        print(f"Generated {variant_name} variant with {len(variant_data)} rows")
