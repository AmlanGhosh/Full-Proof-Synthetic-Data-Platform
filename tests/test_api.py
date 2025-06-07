
import pytest
import asyncio
import pandas as pd
import numpy as np
import io
import sys
import os
from fastapi.testclient import TestClient
from fastapi import UploadFile

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app

client = TestClient(app)

class TestAPI:
    def setup_method(self):
        # Create sample CSV data
        np.random.seed(42)
        self.real_data = pd.DataFrame({
            'age': np.random.randint(18, 80, 100),
            'income': np.random.normal(50000, 15000, 100),
            'gender': np.random.choice(['M', 'F'], 100),
            'target': np.random.binomial(1, 0.3, 100)
        })
        self.synthetic_data = pd.DataFrame({
            'age': np.random.randint(18, 80, 100),
            'income': np.random.normal(52000, 16000, 100),
            'gender': np.random.choice(['M', 'F'], 100),
            'target': np.random.binomial(1, 0.35, 100)
        })
        
        # Convert to CSV strings
        self.real_csv = self.real_data.to_csv(index=False)
        self.synthetic_csv = self.synthetic_data.to_csv(index=False)
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "Full-Proof Synthetic Data Validation Platform API" in response.json()["message"]
    
    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_validate_endpoint(self):
        files = {
            "real_data": ("real.csv", self.real_csv, "text/csv"),
            "synthetic_data": ("synthetic.csv", self.synthetic_csv, "text/csv")
        }
        
        response = client.post("/validate/", files=files)
        assert response.status_code == 200
        
        result = response.json()
        assert result["status"] == "success"
        assert "validation_results" in result
        assert "synthetic_data_quality_score" in result
        assert "data_info" in result
    
    def test_validate_with_config(self):
        files = {
            "real_data": ("real.csv", self.real_csv, "text/csv"),
            "synthetic_data": ("synthetic.csv", self.synthetic_csv, "text/csv")
        }
        
        config = {
            "validators": ["fidelity", "privacy_risk"],
            "target_column": "target",
            "protected_attributes": ["gender"]
        }
        
        response = client.post("/validate/", files=files, json={"config": config})
        assert response.status_code == 200
        
        result = response.json()
        assert "fidelity" in result["validation_results"]
        assert "privacy_risk" in result["validation_results"]
