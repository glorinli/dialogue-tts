# Tests Package

This package contains all test files for the Dialogue TTS system.

## 📁 Test Files

### Core Tests
- **`test_providers_package.py`** - Tests the providers package structure and functionality

### Demos
- **`demo_unified_voices.py`** - Demonstrates the unified voice management system

### Test Runner
- **`run_all_tests.py`** - Runs all tests in the package

## 🚀 Running Tests

### Run All Tests
```bash
python3 tests/run_all_tests.py
```

### Run Individual Tests
```bash
# Test providers package
python3 tests/test_providers_package.py

# Run demo
python3 tests/demo_unified_voices.py
```

### Run Tests from Project Root
```bash
# From the project root directory
python3 -m tests.test_providers_package
python3 -m tests.demo_unified_voices
```

## 🧪 Test Categories

### 1. **Provider Tests**
- Provider package structure
- Provider factory functionality
- Provider registration
- Provider creation

### 2. **Voice Management Tests**
- Unified voice manager
- Voice selection modes (fixed, random, gender_based)
- Provider balancing
- Voice configuration loading

### 3. **TTS Integration Tests**
- Google TTS functionality
- ElevenLabs TTS functionality
- Multi-provider TTS management
- Voice generation

### 4. **Demo Tests**
- Voice distribution demonstration
- Provider balancing demonstration
- Multi-provider conversation examples

## 📊 Test Results

Tests will show:
- ✅ Passed tests
- ❌ Failed tests
- 📊 Summary statistics
- 🔍 Detailed error messages for failed tests

## 🛠️ Adding New Tests

To add a new test:

1. Create a new file in the `tests/` directory
2. Follow the naming convention: `test_*.py`
3. Include proper imports with path adjustment:
   ```python
   import sys
   import os
   sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
   from utils.your_module import your_function
   ```
4. Add the test to `run_all_tests.py` if needed

## 🔧 Troubleshooting

### Import Errors
If you get import errors, make sure:
- Tests are run from the project root directory
- The path adjustment code is included in test files
- All required modules are available

### Path Issues
Tests use relative imports to access the main project modules. The path adjustment code:
```python
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
```
Adds the parent directory (project root) to the Python path.

## 📝 Notes

- Tests are designed to be run from the project root directory
- Some tests require API keys (ElevenLabs) or internet connectivity
- Test output includes detailed information for debugging
- All tests should pass before deploying changes
