
#!/usr/bin/env python3
"""
Setup script to prepare the testing environment
"""

import subprocess
import sys
import os

def install_test_dependencies():
    """Install additional dependencies needed for testing."""
    print("📦 Installing test dependencies...")
    
    test_packages = [
        'pytest',
        'pytest-asyncio', 
        'httpx',
        'requests'
    ]
    
    for package in test_packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

def create_test_directories():
    """Create necessary test directories."""
    print("📁 Creating test directories...")
    
    directories = [
        'tests',
        'test_data',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/ directory")

def main():
    print("🛠️  Setting up test environment...")
    print("=" * 40)
    
    create_test_directories()
    install_test_dependencies()
    
    print("\n✅ Test environment setup complete!")
    print("\nNext steps:")
    print("1. Run tests: python3 test_runner.py")
    print("2. Start API server: python3 -m src.main")
    print("3. Test API: python3 test_runner.py --api-only")

if __name__ == "__main__":
    main()
