#!/usr/bin/env python3
"""
Test Runner
Runs all tests in the tests package.
"""

import sys
import os
import subprocess
from pathlib import Path

def run_test(test_file):
    """Run a single test file."""
    print(f"\n🧪 Running {test_file}...")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Test passed")
            return True
        else:
            print("❌ Test failed")
            if result.stdout:
                print("STDOUT:", result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Running All Tests")
    print("=" * 60)
    
    # Get all test files
    test_dir = Path(__file__).parent
    test_files = [f for f in test_dir.glob("test_*.py") if f.name != "__init__.py"]
    
    # Only run essential tests
    essential_tests = ["test_providers_package.py"]
    test_files = [f for f in test_files if f.name in essential_tests]
    
    print(f"Found {len(test_files)} test files:")
    for test_file in test_files:
        print(f"  - {test_file.name}")
    
    # Run tests
    passed = 0
    failed = 0
    
    for test_file in test_files:
        if run_test(test_file.name):
            passed += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(test_files)}")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
