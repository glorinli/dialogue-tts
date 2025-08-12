#!/usr/bin/env python3
"""
Demo: Unified Voice Management System
Demonstrates how multiple TTS providers can be used in a single conversation.
"""

import json
import os
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.unified_voice_manager import create_unified_voice_manager
from utils.multi_provider_tts import create_multi_provider_tts_manager


def demo_voice_distribution():
    """Demonstrate voice distribution across providers."""
    print("🎭 Voice Distribution Demo")
    print("=" * 50)
    
    # Create voice manager with all providers
    voice_manager = create_unified_voice_manager("gender_based")
    
    # Show available voices
    summary = voice_manager.get_available_voices_summary()
    print("📊 Available Voices:")
    for gender, info in summary.items():
        print(f"  {gender.capitalize()}: {info['total']} total")
        for provider, count in info['providers'].items():
            print(f"    {provider}: {count} voices")
    
    print("\n🎯 Voice Selection Examples:")
    print("-" * 30)
    
    # Simulate a conversation with multiple speakers
    speakers = [
        ("Alice", "female"),
        ("Bob", "male"),
        ("Charlie", "male"),
        ("Diana", "female"),
        ("Eve", "female"),
        ("Frank", "male")
    ]
    
    for speaker_name, gender in speakers:
        voice_config = voice_manager.get_voice_for_speaker(speaker_name, gender)
        print(f"  {speaker_name} ({gender}): {voice_config['voice_name']} ({voice_config['provider']})")
    
    print("\n✨ Notice how voices are distributed across different providers!")


def demo_provider_balancing():
    """Demonstrate provider balancing with weights."""
    print("\n⚖️ Provider Balancing Demo")
    print("=" * 50)
    
    voice_manager = create_unified_voice_manager("gender_based")
    
    # Test provider distribution over multiple selections
    print("🔄 Testing provider distribution over 30 voice selections...")
    
    male_providers = []
    female_providers = []
    
    for i in range(30):
        male_voice = voice_manager.get_voice_for_speaker(f"Speaker{i}", "male")
        female_voice = voice_manager.get_voice_for_speaker(f"Speaker{i}", "female")
        
        male_providers.append(male_voice['provider'])
        female_providers.append(female_voice['provider'])
    
    # Count provider usage
    from collections import Counter
    
    male_counts = Counter(male_providers)
    female_counts = Counter(female_providers)
    
    print("\n📈 Male Voice Distribution:")
    total_male = sum(male_counts.values())
    for provider, count in male_counts.items():
        percentage = (count / total_male) * 100
        print(f"  {provider}: {count}/{total_male} ({percentage:.1f}%)")
    
    print("\n📈 Female Voice Distribution:")
    total_female = sum(female_counts.values())
    for provider, count in female_counts.items():
        percentage = (count / total_female) * 100
        print(f"  {provider}: {count}/{total_female} ({percentage:.1f}%)")
    
    print("\n🎯 The system automatically balances voices across providers!")


def demo_voice_modes():
    """Demonstrate different voice selection modes."""
    print("\n🎲 Voice Selection Modes Demo")
    print("=" * 50)
    
    modes = ["gender_based", "random", "fixed"]
    speakers = [("Alice", "female"), ("Bob", "male")]
    
    for mode in modes:
        print(f"\n📋 {mode.upper()} Mode:")
        print("-" * 20)
        
        voice_manager = create_unified_voice_manager(mode)
        
        for speaker_name, gender in speakers:
            voice_config = voice_manager.get_voice_for_speaker(speaker_name, gender)
            print(f"  {speaker_name}: {voice_config['voice_name']} ({voice_config['provider']})")
        
        if mode == "fixed":
            print("  🔒 Same speaker always gets same voice")
        elif mode == "random":
            print("  🎲 Random voice selection each time")
        else:  # gender_based
            print("  ⚖️ Balanced selection across providers")


def demo_multi_provider_conversation():
    """Demonstrate how a single conversation can use multiple providers."""
    print("\n🗣️ Multi-Provider Conversation Demo")
    print("=" * 50)
    
    # Sample conversation
    conversation = {
        "speakers": {
            "Alice": {"gender": "female"},
            "Bob": {"gender": "male"},
            "Charlie": {"gender": "male"},
            "Diana": {"gender": "female"}
        },
        "content": "Alice: Hello everyone! Bob: Hi Alice! Charlie: Good morning! Diana: Hello there!"
    }
    
    print("📝 Sample Conversation:")
    print("  Alice (female): Hello everyone!")
    print("  Bob (male): Hi Alice!")
    print("  Charlie (male): Good morning!")
    print("  Diana (female): Hello there!")
    
    print("\n🎭 Voice Assignments (Gender-based mode):")
    print("-" * 40)
    
    voice_manager = create_unified_voice_manager("gender_based")
    
    for speaker_name, speaker_info in conversation["speakers"].items():
        gender = speaker_info["gender"]
        voice_config = voice_manager.get_voice_for_speaker(speaker_name, gender)
        print(f"  {speaker_name} ({gender}): {voice_config['voice_name']} ({voice_config['provider']})")
    
    print("\n✨ Notice how different speakers can use different TTS providers!")
    print("   This allows for optimal voice quality and variety in a single conversation.")


def main():
    """Run all demos."""
    print("🚀 Unified Voice Management System Demo")
    print("=" * 60)
    print("This demo shows how the new system supports multiple TTS providers")
    print("in a single conversation with intelligent voice distribution.\n")
    
    # Run all demos
    demo_voice_distribution()
    demo_provider_balancing()
    demo_voice_modes()
    demo_multi_provider_conversation()
    
    print("\n🎉 Demo Complete!")
    print("\n💡 Key Benefits:")
    print("  ✅ Multiple TTS providers in one conversation")
    print("  ✅ Gender-based voice organization")
    print("  ✅ Automatic provider balancing")
    print("  ✅ Flexible voice selection modes")
    print("  ✅ Fallback to available providers only")
    print("\n🔧 To test with ElevenLabs, set ELEVENLABS_API_KEY in .env file")


if __name__ == "__main__":
    main()
