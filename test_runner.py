
#!/usr/bin/env python3
"""
Comprehensive test runner for Full-Proof Synthetic Data Validation Platform
"""

import os
import sys
import subprocess
import pandas as pd
import numpy as np
import requests
import time
import json
from pathlib import Path

def create_sample_data():
    """Create sample datasets for testing."""
    print("📊 Creating sample test datasets...")
    
    # Create data directory
    data_dir = Path("test_data")
    data_dir.mkdir(exist_ok=True)
    
    # Generate real dataset
    np.random.seed(42)
    real_data = pd.DataFrame({
        'age': np.random.randint(18, 80, 1000),
        'income': np.random.normal(50000, 15000, 1000),
        'gender': np.random.choice(['M', 'F'], 1000),
        'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], 1000),
        'target': np.random.binomial(1, 0.3, 1000)
    })
    
    # Generate synthetic dataset (slightly different distribution)
    synthetic_data = pd.DataFrame({
        'age': np.random.randint(18, 80, 1000),
        'income': np.random.normal(52000, 16000, 1000),
        'gender': np.random.choice(['M', 'F'], 1000),
        'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], 1000),
        'target': np.random.binomial(1, 0.35, 1000)
    })
    
    # Save datasets
    real_data.to_csv(data_dir / "real_data.csv", index=False)
    synthetic_data.to_csv(data_dir / "synthetic_data.csv", index=False)
    
    print(f"✅ Sample datasets created in {data_dir}/")
    return data_dir / "real_data.csv", data_dir / "synthetic_data.csv"

def run_unit_tests():
    """Run unit tests using pytest."""
    print("🧪 Running unit tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✅ Unit tests passed!")
            return True
        else:
            print("❌ Unit tests failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error running unit tests: {e}")
        return False

def test_api_endpoints(base_url="http://localhost:5000"):
    """Test API endpoints."""
    print("🌐 Testing API endpoints...")
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test root endpoint
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
        
        # Test validation endpoint
        real_path, synthetic_path = create_sample_data()
        
        with open(real_path, 'rb') as real_file, open(synthetic_path, 'rb') as synthetic_file:
            files = {
                'real_data': ('real.csv', real_file, 'text/csv'),
                'synthetic_data': ('synthetic.csv', synthetic_file, 'text/csv')
            }
            
            response = requests.post(f"{base_url}/validate/", files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Validation endpoint working")
                print(f"   Overall Quality Score: {result.get('synthetic_data_quality_score', {}).get('overall_synthetic_data_quality_score', 'N/A')}")
                return True
            else:
                print(f"❌ Validation endpoint failed: {response.status_code}")
                if response.text:
                    print(f"   Error: {response.text}")
                return False
                
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure it's running on port 5000.")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_individual_validators():
    """Test individual validator modules."""
    print("🔍 Testing individual validator modules...")
    
    try:
        # Add src to path
        sys.path.append('src')
        
        from validator_modules.fidelity import FidelityValidator
        from validator_modules.privacy_risk import PrivacyRiskValidator
        
        # Create test data
        real_data = pd.DataFrame({
            'col1': np.random.normal(0, 1, 100),
            'col2': np.random.normal(0, 1, 100)
        })
        synthetic_data = pd.DataFrame({
            'col1': np.random.normal(0.1, 1.1, 100),
            'col2': np.random.normal(0.1, 1.1, 100)
        })
        
        # Test Fidelity Validator
        fidelity_validator = FidelityValidator()
        fidelity_result = fidelity_validator.validate(real_data, synthetic_data)
        if 'fidelity_score' in fidelity_result:
            print(f"✅ Fidelity Validator working (score: {fidelity_result['fidelity_score']:.3f})")
        else:
            print("❌ Fidelity Validator failed")
            return False
        
        # Test Privacy Risk Validator
        privacy_validator = PrivacyRiskValidator()
        privacy_result = privacy_validator.validate(real_data, synthetic_data)
        if 'privacy_risk_score' in privacy_result:
            print(f"✅ Privacy Risk Validator working (score: {privacy_result['privacy_risk_score']:.3f})")
        else:
            print("❌ Privacy Risk Validator failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing individual validators: {e}")
        return False

def main():
    """Main test runner."""
    print("🚀 Full-Proof Synthetic Data Validation Platform - Test Suite")
    print("=" * 60)
    
    # Test results
    results = {}
    
    # 1. Create sample data
    try:
        create_sample_data()
        results['sample_data'] = True
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
        results['sample_data'] = False
    
    # 2. Test individual validators
    results['validators'] = test_individual_validators()
    
    # 3. Run unit tests
    results['unit_tests'] = run_unit_tests()
    
    # 4. Test API (if server is running)
    print("\n⚠️  To test the API endpoints:")
    print("   1. Start the server: python3 -m src.main")
    print("   2. Run: python3 test_runner.py --api-only")
    
    if '--api-only' in sys.argv:
        results['api_tests'] = test_api_endpoints()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    # Overall result
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All tests passed! Your codebase is ready.")
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
