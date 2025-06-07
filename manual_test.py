
#!/usr/bin/env python3
"""
Manual testing script for quick validation
"""

import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append('src')

def test_core_functionality():
    """Test core functionality without API."""
    print("🔧 Testing core functionality...")
    
    try:
        from orchestrator import ValidationOrchestrator
        from aggregator import ScoreAggregator
        
        # Create test data
        np.random.seed(42)
        real_data = pd.DataFrame({
            'age': np.random.randint(18, 80, 200),
            'income': np.random.normal(50000, 15000, 200),
            'target': np.random.binomial(1, 0.3, 200)
        })
        
        synthetic_data = pd.DataFrame({
            'age': np.random.randint(18, 80, 200),
            'income': np.random.normal(52000, 16000, 200),
            'target': np.random.binomial(1, 0.35, 200)
        })
        
        print(f"Real data shape: {real_data.shape}")
        print(f"Synthetic data shape: {synthetic_data.shape}")
        
        # Test orchestrator
        orchestrator = ValidationOrchestrator()
        config = {
            'validators': ['fidelity', 'privacy_risk'],
            'target_column': 'target'
        }
        
        print("\n⏳ Running validation pipeline...")
        results = orchestrator.run_validation_pipeline(real_data, synthetic_data, config)
        
        print("✅ Validation completed!")
        print(f"Available results: {list(results.keys())}")
        
        # Test aggregator
        aggregator = ScoreAggregator()
        quality_score = aggregator.calculate_synthetic_data_quality_score(results)
        
        print(f"\n📊 Overall Quality Score: {quality_score.get('overall_synthetic_data_quality_score', 'N/A'):.3f}")
        print(f"Quality Grade: {quality_score.get('quality_grade', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in core functionality test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Manual Test Suite")
    print("=" * 30)
    
    success = test_core_functionality()
    
    if success:
        print("\n🎉 Manual test passed! Core functionality is working.")
    else:
        print("\n❌ Manual test failed. Check the error messages above.")
