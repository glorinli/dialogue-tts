# Unified Voice Management System

## Overview

The Dialogue TTS system has been refactored to support **multiple TTS providers in a single conversation** with intelligent voice distribution and gender-based organization.

## 🏗️ New Architecture

### Before (Provider-Separated)
```
Voice Manager → Single Provider → Voice Selection
     ↓
Google TTS Provider (separate voices)
ElevenLabs TTS Provider (separate voices)
```

### After (Unified)
```
Unified Voice Manager → Multi-Provider TTS Manager
     ↓                           ↓
All voices organized by gender    Routes to appropriate provider
     ↓                           ↓
Google + ElevenLabs voices       Google TTS Provider
     ↓                           ElevenLabs TTS Provider
Intelligent provider balancing
```

## 🎯 Key Features

### 1. **Unified Voice Pool**
- All voices from all providers are merged into two lists: `male` and `female`
- No more provider-specific voice files
- Single configuration file: `providers/configs/unified_voices.json`

### 2. **Multi-Provider Support**
- Single conversation can use multiple TTS providers
- Automatic provider selection based on voice availability
- Fallback to available providers only

### 3. **Intelligent Voice Distribution**
- Provider balancing with configurable weights
- Gender-based voice organization
- Multiple selection modes: `fixed`, `random`, `gender_based`

### 4. **Automatic Provider Management**
- Detects available providers at runtime
- Filters voices to only include available providers
- Handles provider initialization failures gracefully

## 📁 New File Structure

```
utils/
├── unified_voice_manager.py      # Unified voice management
└── multi_provider_tts.py         # Multi-provider TTS routing

providers/
├── configs/
│   └── unified_voices.json      # All voices in one place
├── base.py                       # Abstract TTS provider interface
├── factory.py                    # Provider factory
├── google.py                     # Google TTS implementation
├── elevenlabs.py                 # ElevenLabs TTS implementation
└── registry.py                   # Provider registration
```

## 🔧 Configuration

### Unified Voice Configuration (`unified_voices.json`)

```json
{
    "voices": {
        "male": [
            {
                "name": "en-US-male-David",
                "provider": "google",
                "tld": "com",
                "description": "Canadian male voice"
            },
            {
                "name": "en-US-male-Adam",
                "provider": "elevenlabs",
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "description": "Deep, confident male voice"
            }
        ],
        "female": [
            {
                "name": "en-US-female-Sarah",
                "provider": "google",
                "tld": "com",
                "description": "US female voice"
            },
            {
                "name": "en-US-female-Rachel",
                "provider": "elevenlabs",
                "voice_id": "21m00Tcm4TlvDq8ikWAM",
                "description": "Clear, professional female voice"
            }
        ]
    },
    "default_provider": "google",
    "provider_weights": {
        "google": 0.5,
        "elevenlabs": 0.5
    }
}
```

## 🚀 Usage Examples

### Basic Usage (No Changes Required)

```python
# The existing API still works exactly the same
tts_tool = DialogueTTS(voice_mode="gender_based")
output = tts_tool.process_conversation(conversation_data)
```

### Voice Selection Modes

```python
# Gender-based with provider balancing
voice_manager = create_unified_voice_manager("gender_based")

# Random selection
voice_manager = create_unified_voice_manager("random")

# Fixed assignment (same speaker = same voice)
voice_manager = create_unified_voice_manager("fixed")
```

### Multi-Provider Conversation

```python
# A single conversation can now use multiple providers automatically
conversation = {
    "speakers": {
        "Alice": {"gender": "female"},
        "Bob": {"gender": "male"},
        "Charlie": {"gender": "male"}
    },
    "content": "Alice: Hello! Bob: Hi! Charlie: Good morning!"
}

# Voices will be automatically distributed across available providers
# Alice might get a Google voice, Bob an ElevenLabs voice, etc.
```

## 📊 Benefits

### 1. **Better Voice Variety**
- More voices available per gender
- Automatic provider balancing
- No more provider lock-in

### 2. **Improved Quality**
- Use best voice for each speaker
- Mix high-quality (ElevenLabs) with free (Google) voices
- Optimal voice selection per use case

### 3. **Simplified Management**
- Single voice configuration file
- Automatic provider detection
- No need to manage provider-specific voice files

### 4. **Extensibility**
- Easy to add new TTS providers
- Simple voice configuration
- Provider-agnostic voice management

## 🔄 Migration Guide

### For Existing Users
- **No changes required** - existing code continues to work
- The system automatically detects available providers
- Voice selection is now more intelligent and varied

### For New Implementations
- Use `unified_voices.json` for voice configuration
- Leverage multi-provider capabilities for better voice variety
- Consider provider weights for optimal distribution

## 🧪 Testing

### Run the Demo
```bash
python3 demo_unified_voices.py
```

### Test the System
```bash
python3 test_unified_voices.py
```

### Test with Main Application
```bash
python3 main.py examples/conversation1.json --provider google --verbose
```

## 🔮 Future Enhancements

### Planned Features
1. **Dynamic Provider Weights**: Adjust weights based on voice quality or cost
2. **Voice Quality Scoring**: Automatically select best available voices
3. **Provider Fallback**: Automatic fallback if preferred provider fails
4. **Voice Cloning**: Support for custom voice cloning across providers

### Easy to Add
- New TTS providers (Azure, AWS, etc.)
- Custom voice configurations
- Advanced voice selection algorithms
- Provider-specific optimizations

## 📝 Summary

The new Unified Voice Management System transforms the Dialogue TTS from a single-provider tool into a **multi-provider, intelligent voice orchestration system**. It maintains backward compatibility while providing:

- **Multiple TTS providers in one conversation**
- **Gender-based voice organization**
- **Automatic provider balancing**
- **Intelligent voice selection**
- **Easy extensibility**

This refactoring represents a significant architectural improvement that makes the system more powerful, flexible, and maintainable while preserving all existing functionality.
