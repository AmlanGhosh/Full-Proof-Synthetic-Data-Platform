
"""
FastAPI application with /validate/ API endpoint.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import io
from typing import Dict, Any
from src.loader import DataLoader
from src.orchestrator import ValidationOrchestrator
from src.aggregator import ScoreAggregator

app = FastAPI(title="Full-Proof Synthetic Data Validation Platform", version="1.0.0")

# Initialize components
data_loader = DataLoader()
orchestrator = ValidationOrchestrator()
aggregator = ScoreAggregator()

@app.get("/")
async def root():
    return {"message": "Full-Proof Synthetic Data Validation Platform API"}

@app.post("/validate/")
async def validate_synthetic_data(
    real_data: UploadFile = File(...),
    synthetic_data: UploadFile = File(...),
    config: Dict[str, Any] = None
):
    """
    Validate synthetic data against real data.
    
    Parameters:
    - real_data: CSV file containing real dataset
    - synthetic_data: CSV file containing synthetic dataset
    - config: Validation configuration (optional)
    """
    try:
        # Default configuration
        if config is None:
            config = {
                'validators': ['fidelity', 'privacy_risk'],
                'target_column': None,
                'protected_attributes': [],
                'treatment_column': None,
                'outcome_column': None,
                'causal_variables': []
            }
        
        # Load real data
        real_content = await real_data.read()
        real_df = pd.read_csv(io.StringIO(real_content.decode('utf-8')))
        
        # Load synthetic data
        synthetic_content = await synthetic_data.read()
        synthetic_df = pd.read_csv(io.StringIO(synthetic_content.decode('utf-8')))
        
        # Run validation pipeline
        validation_results = orchestrator.run_validation_pipeline(
            real_df, synthetic_df, config
        )
        
        # Aggregate scores
        final_scores = aggregator.calculate_synthetic_data_quality_score(validation_results)
        
        return JSONResponse(content={
            'status': 'success',
            'validation_results': validation_results,
            'synthetic_data_quality_score': final_scores,
            'data_info': {
                'real_data_shape': real_df.shape,
                'synthetic_data_shape': synthetic_df.shape,
                'columns': list(real_df.columns)
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Synthetic Data Validation Platform"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
