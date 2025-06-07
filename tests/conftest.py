
import pytest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture to provide test data directory path."""
    return os.path.join(os.path.dirname(__file__), 'test_data')

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before running tests."""
    # Create test data directory if it doesn't exist
    test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(test_data_dir, exist_ok=True)
    
    print("Test environment setup complete")
    yield
    print("Test environment cleanup complete")
