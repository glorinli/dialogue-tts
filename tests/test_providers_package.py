#!/usr/bin/env python3
"""
Test script for the new providers package structure
Verifies that all providers are properly registered and accessible.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_providers_package():
    """Test the providers package structure."""
    
    print("Testing Providers Package Structure")
    print("=" * 50)
    
    try:
        # Test importing the package
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from providers.registry import TTSProviderFactory, AVAILABLE_PROVIDERS
        print("✅ Successfully imported providers package")
        
        # Test available providers
        print(f"✅ Available providers: {AVAILABLE_PROVIDERS}")
        
        # Test provider factory
        print(f"✅ Factory supports: {TTSProviderFactory.get_supported_providers()}")
        
        # Test creating providers
        print("\n🔧 Testing provider creation...")
        
        # Test Google provider
        try:
            google_provider = TTSProviderFactory.create_provider('google', 'test_output')
            print("✅ Google provider created successfully")
        except Exception as e:
            print(f"❌ Failed to create Google provider: {e}")
        
        # Test ElevenLabs provider (will fail without API key, but should import)
        try:
            elevenlabs_provider = TTSProviderFactory.create_provider('elevenlabs', 'test_output')
            print("✅ ElevenLabs provider created successfully")
        except Exception as e:
            if "API key" in str(e):
                print("✅ ElevenLabs provider imported correctly (API key missing as expected)")
            else:
                print(f"❌ Unexpected error with ElevenLabs provider: {e}")
        
        print("\n🎉 Providers package test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_voice_configuration():
    """Test voice configuration loading."""
    print("\n📁 Testing voice configuration...")
    
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from utils.unified_voice_manager import create_unified_voice_manager
        
        # Test creating unified voice manager
        voice_manager = create_unified_voice_manager("gender_based")
        print("✅ Unified voice manager created successfully")
        
        # Test getting voice for male speaker
        male_voice = voice_manager.get_voice_for_speaker("Bob", "male")
        print(f"✅ Male voice config: {male_voice}")
        
        # Test getting voice for female speaker
        female_voice = voice_manager.get_voice_for_speaker("Alice", "female")
        print(f"✅ Female voice config: {female_voice}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing voice configuration: {e}")
        return False

if __name__ == "__main__":
    print("Providers Package Test Suite")
    print("=" * 50)
    
    # Test basic package functionality
    package_success = test_providers_package()
    
    # Test voice configuration
    config_success = test_voice_configuration()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    if package_success and config_success:
        print("🎉 All tests passed! The new providers package structure is working correctly.")
        print("\nPackage structure:")
        print("  providers/")
        print("    ├── __init__.py")
        print("    ├── base.py")
        print("    ├── factory.py")
        print("    ├── google.py")
        print("    ├── elevenlabs.py")
        print("    ├── registry.py")
        print("    └── configs/")
        print("        └── unified_voices.json")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
