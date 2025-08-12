#!/usr/bin/env python3
"""
Test script for ElevenLabs TTS integration
Tests the ElevenLabs TTS provider with different voices.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from providers.registry import ElevenLabsTTSProvider, TTSProviderFactory

def test_elevenlabs_provider():
    """Test the ElevenLabs TTS provider."""
    
    # Check if API key is set
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ ELEVENLABS_API_KEY not found in .env file")
        print("Please create a .env file with your ElevenLabs API key:")
        print("ELEVENLABS_API_KEY=your_api_key_here")
        return False
    
    print("✅ ElevenLabs API key found")
    
    # Create output directory
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Test creating provider through factory
        print("\n🔧 Testing TTS Provider Factory...")
        provider = TTSProviderFactory.create_provider('elevenlabs', output_dir)
        print("✅ ElevenLabs provider created successfully")
        
        # Test getting supported voices
        print("\n🎤 Testing voice information...")
        voices = provider.get_supported_voices()
        print(f"✅ Found {len(voices)} available voices")
        
        # Show some voice details
        for i, (name, info) in enumerate(list(voices.items())[:3]):
            print(f"  {i+1}. {name}: {info.get('labels', {})}")
        
        # Test speech generation
        print("\n🎵 Testing speech generation...")
        
        # Test male voice
        print("  Testing male voice...")
        male_result = provider.generate_speech(
            "Hello, this is a test of the male voice from ElevenLabs.",
            "TestMale",
            "male"
        )
        
        if male_result:
            print(f"  ✅ Male voice generated: {os.path.basename(male_result)}")
        else:
            print("  ❌ Male voice generation failed")
        
        # Test female voice
        print("  Testing female voice...")
        female_result = provider.generate_speech(
            "Hello, this is a test of the female voice from ElevenLabs.",
            "TestFemale",
            "female"
        )
        
        if female_result:
            print(f"  ✅ Female voice generated: {os.path.basename(female_result)}")
        else:
            print("  ❌ Female voice generation failed")
        
        print(f"\n🎉 Test completed! Check the '{output_dir}' directory for generated audio files.")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def test_voice_configuration():
    """Test voice configuration loading."""
    print("\n📁 Testing voice configuration...")
    
    try:
        from utils.unified_voice_manager import create_unified_voice_manager
        
        # Test creating voice manager for ElevenLabs
        voice_manager = create_unified_voice_manager("gender_based")
        
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
    print("ElevenLabs TTS Integration Test")
    print("=" * 50)
    
    # Test basic provider functionality
    provider_success = test_elevenlabs_provider()
    
    # Test voice configuration
    config_success = test_voice_configuration()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    if provider_success and config_success:
        print("🎉 All tests passed! ElevenLabs integration is working correctly.")
        print("\nTo use ElevenLabs in your conversations:")
        print("  python main.py examples/conversation1.json --provider elevenlabs")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        
        if not provider_success:
            print("\nProvider test failed. Check your API key and internet connection.")
        if not config_success:
            print("\nVoice configuration test failed. Check the voice configuration files.")
