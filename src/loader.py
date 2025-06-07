
"""
Real-time data loading module for CSV files.
Handles data ingestion and preprocessing for validation pipeline.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import logging

class DataLoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """Load CSV file and return pandas DataFrame."""
        try:
            df = pd.read_csv(file_path)
            self.logger.info(f"Successfully loaded {len(df)} rows from {file_path}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading CSV file {file_path}: {str(e)}")
            raise
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Basic preprocessing of loaded data."""
        # Handle missing values
        df = df.dropna()
        
        # Basic data type inference
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except ValueError:
                    pass  # Keep as string if not numeric
        
        return df
    
    def load_real_time_data(self, file_path: str) -> Dict[str, Any]:
        """Load and preprocess data for real-time validation."""
        df = self.load_csv(file_path)
        processed_df = self.preprocess_data(df)
        
        return {
            'data': processed_df,
            'shape': processed_df.shape,
            'columns': list(processed_df.columns),
            'dtypes': processed_df.dtypes.to_dict()
        }
