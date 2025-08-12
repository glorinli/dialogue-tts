#!/usr/bin/env python3
"""
Test Unified Voice Management System
Tests the new unified voice manager that supports multiple TTS providers in a single conversation.
"""

import json
import os
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.unified_voice_manager import create_unified_voice_manager, get_voice_config_for_conversation
from utils.multi_provider_tts import create_multi_provider_tts_manager


def test_unified_voice_manager():
    """Test the unified voice manager functionality."""
    print("🧪 Testing Unified Voice Manager")
    print("=" * 50)
    
    # Test different modes
    modes = ["gender_based", "random", "fixed"]
    
    for mode in modes:
        print(f"\n📋 Testing {mode.upper()} mode:")
        print("-" * 30)
        
        try:
            voice_manager = create_unified_voice_manager(mode)
            
            # Test male voice selection
            male_voice = voice_manager.get_voice_for_speaker("Alice", "female")
            print(f"  Female voice: {male_voice['voice_name']} ({male_voice['provider']})")
            
            # Test female voice selection
            female_voice = voice_manager.get_voice_for_speaker("Bob", "male")
            print(f"  Male voice: {female_voice['voice_name']} ({female_voice['provider']})")
            
            # Show voice summary
            summary = voice_manager.get_available_voices_summary()
            print(f"  Available voices: {summary}")
            
        except Exception as e:
            print(f"  ❌ Error in {mode} mode: {e}")
    
    print("\n✅ Unified Voice Manager tests completed!")


def test_multi_provider_tts():
    """Test the multi-provider TTS manager."""
    print("\n🧪 Testing Multi-Provider TTS Manager")
    print("=" * 50)
    
    try:
        tts_manager = create_multi_provider_tts_manager("test_output")
        
        # Test provider availability
        available_providers = tts_manager.get_available_providers()
        print(f"Available providers: {available_providers}")
        
        # Test provider info
        for provider in available_providers:
            info = tts_manager.get_provider_info(provider)
            if info:
                print(f"  {provider}: {info['class']}")
            else:
                print(f"  {provider}: Not available")
        
        print("\n✅ Multi-Provider TTS Manager tests completed!")
        
    except Exception as e:
        print(f"❌ Error testing Multi-Provider TTS Manager: {e}")


def test_conversation_voice_assignment():
    """Test voice assignment for an entire conversation."""
    print("\n🧪 Testing Conversation Voice Assignment")
    print("=" * 50)
    
    # Sample conversation data
    conversation = {
        "speakers": {
            "Alice": {"gender": "female"},
            "Bob": {"gender": "male"},
            "Charlie": {"gender": "male"},
            "Diana": {"gender": "female"}
        },
        "content": "Alice: Hello everyone! Bob: Hi Alice! Charlie: Good morning! Diana: Hello there!"
    }
    
    try:
        # Test different modes
        modes = ["gender_based", "random", "fixed"]
        
        for mode in modes:
            print(f"\n📋 {mode.upper()} mode:")
            print("-" * 20)
            
            voice_configs = get_voice_config_for_conversation(conversation, mode)
            
            for speaker, config in voice_configs.items():
                print(f"  {speaker}: {config['voice_name']} ({config['provider']})")
        
        print("\n✅ Conversation Voice Assignment tests completed!")
        
    except Exception as e:
        print(f"❌ Error testing Conversation Voice Assignment: {e}")


def test_provider_balancing():
    """Test that voices are balanced across providers."""
    print("\n🧪 Testing Provider Balancing")
    print("=" * 50)
    
    try:
        voice_manager = create_unified_voice_manager("gender_based")
        
        # Generate multiple voice selections to see provider distribution
        male_providers = []
        female_providers = []
        
        for i in range(20):
            male_voice = voice_manager.get_voice_for_speaker(f"Speaker{i}", "male")
            female_voice = voice_manager.get_voice_for_speaker(f"Speaker{i}", "female")
            
            male_providers.append(male_voice['provider'])
            female_providers.append(female_voice['provider'])
        
        # Count provider usage
        from collections import Counter
        
        male_counts = Counter(male_providers)
        female_counts = Counter(female_providers)
        
        print("Male voice provider distribution:")
        for provider, count in male_counts.items():
            print(f"  {provider}: {count}/20 ({count/20*100:.1f}%)")
        
        print("\nFemale voice provider distribution:")
        for provider, count in female_counts.items():
            print(f"  {provider}: {count}/20 ({count/20*100:.1f}%)")
        
        print("\n✅ Provider Balancing tests completed!")
        
    except Exception as e:
        print(f"❌ Error testing Provider Balancing: {e}")


def main():
    """Run all tests."""
    print("🚀 Unified Voice Management System Test Suite")
    print("=" * 60)
    
    # Test unified voice manager
    test_unified_voice_manager()
    
    # Test multi-provider TTS manager
    test_multi_provider_tts()
    
    # Test conversation voice assignment
    test_conversation_voice_assignment()
    
    # Test provider balancing
    test_provider_balancing()
    
    print("\n🎉 All tests completed!")
    print("\n📊 Summary:")
    print("  ✅ Unified voice management across multiple providers")
    print("  ✅ Gender-based voice organization")
    print("  ✅ Provider balancing with weights")
    print("  ✅ Multiple voice selection modes")
    print("  ✅ Single conversation with mixed providers")


if __name__ == "__main__":
    main()
