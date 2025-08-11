#!/usr/bin/env python3
"""
Voice management utilities
Handles gender-based voice selection with fixed and random options.
"""

import json
import os
import random
from typing import Dict, List, Optional, Any
from enum import Enum


class VoiceSelectionMode(Enum):
    """Voice selection modes."""
    FIXED = "fixed"      # Use specific voice for each speaker
    RANDOM = "random"    # Randomly select from available voices
    GENDER_BASED = "gender_based"  # Select based on gender only


class VoiceManager:
    """Manages voice selection for different speakers and genders."""
    
    def __init__(self, mode: VoiceSelectionMode = VoiceSelectionMode.GENDER_BASED, provider: str = "google"):
        self.mode = mode
        self.provider = provider
        self.voice_cache = {}  # Cache for fixed voice assignments
        self.available_voices = self._initialize_voice_pool(provider)
    
    def _initialize_voice_pool(self, provider: str = "google") -> Dict[str, List[Dict]]:
        """Initialize the pool of available voices by gender for a specific provider."""
        # Load main config to get provider mapping
        main_config_path = os.path.join(os.path.dirname(__file__), 'voice_config.json')
        
        try:
            with open(main_config_path, 'r') as f:
                main_config = json.load(f)
                provider_file = main_config.get('voice_mapping', {}).get(provider, 'google_voices.json')
        except (FileNotFoundError, json.JSONDecodeError):
            provider_file = 'google_voices.json'
        
        # Load provider-specific voice file
        provider_config_path = os.path.join(os.path.dirname(__file__), provider_file)
        
        try:
            with open(provider_config_path, 'r') as f:
                provider_config = json.load(f)
                return provider_config.get('voices', {})
        except (FileNotFoundError, json.JSONDecodeError):
            # Fallback to default voices if config file is not found or invalid
            return {
                "male": [
                    {"name": "en-US-male-David", "tld": "ca", "description": "Canadian male voice"},
                    {"name": "en-US-male-Michael", "tld": "ie", "description": "Irish male voice"}
                ],
                "female": [
                    {"name": "en-US-female-Sarah", "tld": "com", "description": "US female voice"},
                    {"name": "en-US-female-Emma", "tld": "ca", "description": "Canadian female voice"}
                ]
            }
    
    def get_voice_for_speaker(self, speaker_name: str, gender: str, 
                            provider: str = "google") -> Dict[str, Any]:
        """
        Get voice configuration for a speaker.
        
        Args:
            speaker_name: Name of the speaker
            gender: Gender of the speaker ('male' or 'female')
            provider: TTS provider name
        
        Returns:
            Dictionary with voice configuration
        """
        if self.mode == VoiceSelectionMode.FIXED:
            return self._get_fixed_voice(speaker_name, gender, provider)
        elif self.mode == VoiceSelectionMode.RANDOM:
            return self._get_random_voice(gender, provider)
        else:  # GENDER_BASED
            return self._get_gender_based_voice(gender, provider)
    
    def _get_fixed_voice(self, speaker_name: str, gender: str, 
                        provider: str) -> Dict[str, Any]:
        """Get or assign a fixed voice for a speaker."""
        cache_key = f"{speaker_name}_{gender}_{provider}"
        
        if cache_key not in self.voice_cache:
            # Assign a new voice for this speaker
            available_voices = self.available_voices.get(gender, [])
            if available_voices:
                selected_voice = random.choice(available_voices)
                self.voice_cache[cache_key] = selected_voice
            else:
                # Fallback to default voice
                self.voice_cache[cache_key] = self._get_default_voice(gender, provider)
        
        return {
            "voice_name": self.voice_cache[cache_key]["name"],
            "tld": self.voice_cache[cache_key].get("tld"),
            "gender": gender,
            "provider": provider,
            "mode": "fixed"
        }
    
    def _get_random_voice(self, gender: str, provider: str) -> Dict[str, Any]:
        """Get a random voice for the gender."""
        available_voices = self.available_voices.get(gender, [])
        if available_voices:
            selected_voice = random.choice(available_voices)
        else:
            selected_voice = self._get_default_voice(gender, provider)
        
        return {
            "voice_name": selected_voice["name"],
            "tld": selected_voice.get("tld"),
            "gender": gender,
            "provider": provider,
            "mode": "random"
        }
    
    def _get_gender_based_voice(self, gender: str, provider: str) -> Dict[str, Any]:
        """Get a gender-appropriate voice."""
        # For gender-based selection, use consistent voices from the config
        available_voices = self.available_voices.get(gender, [])
        
        if available_voices:
            # Use the first available voice for consistency
            selected_voice = available_voices[0]
            return {
                "voice_name": selected_voice["name"],
                "tld": selected_voice.get("tld"),
                "gender": gender,
                "provider": provider,
                "mode": "gender_based"
            }
        else:
            # Fallback to default voice
            default_voice = self._get_default_voice(gender, provider)
            return {
                "voice_name": default_voice["name"],
                "tld": default_voice.get("tld"),
                "gender": gender,
                "provider": provider,
                "mode": "gender_based"
            }
    
    def _get_default_voice(self, gender: str, provider: str) -> Dict[str, str]:
        """Get default voice for gender and provider."""
        if provider == "google":
            default_name = f"en-US-{gender}-Default"
            default_tld = "com" if gender == "female" else "ca"
            return {
                "name": default_name,
                "tld": default_tld,
                "description": f"Default {gender} voice"
            }
        else:
            # Default fallback
            return {
                "name": f"en-US-{gender}-Default",
                "tld": "com",
                "description": f"Default {gender} voice"
            }
    
    def set_voice_pool(self, gender: str, voices: List[str]):
        """Set custom voice pool for a gender."""
        self.available_voices[gender] = voices
    
    def add_voice_to_pool(self, gender: str, voice: str):
        """Add a voice to the pool for a gender."""
        if gender not in self.available_voices:
            self.available_voices[gender] = []
        self.available_voices[gender].append(voice)
    
    def clear_voice_cache(self):
        """Clear the voice assignment cache."""
        self.voice_cache.clear()
    
    def get_voice_info(self, speaker_name: str, gender: str, 
                      provider: str = "google") -> Dict[str, Any]:
        """Get detailed voice information for a speaker."""
        voice_config = self.get_voice_for_speaker(speaker_name, gender, provider)
        
        return {
            "speaker_name": speaker_name,
            "gender": gender,
            "provider": provider,
            "voice_name": voice_config["voice_name"],
            "selection_mode": voice_config["mode"],
            "available_voices": len(self.available_voices.get(gender, [])),
            "cached": f"{speaker_name}_{gender}_{provider}" in self.voice_cache
        }


def create_voice_manager(mode: str = "gender_based", 
                        provider: str = "google",
                        custom_voices: Optional[Dict[str, List[str]]] = None) -> VoiceManager:
    """
    Create a voice manager with specified configuration.
    
    Args:
        mode: Voice selection mode ('fixed', 'random', 'gender_based')
        provider: TTS provider name
        custom_voices: Custom voice pool configuration
    
    Returns:
        Configured VoiceManager instance
    """
    try:
        voice_mode = VoiceSelectionMode(mode.lower())
    except ValueError:
        print(f"Invalid voice mode '{mode}', using 'gender_based'")
        voice_mode = VoiceSelectionMode.GENDER_BASED
    
    manager = VoiceManager(voice_mode, provider)
    
    if custom_voices:
        for gender, voices in custom_voices.items():
            manager.set_voice_pool(gender, voices)
    
    return manager


def get_voice_config_for_conversation(speakers: List[Dict], 
                                    voice_mode: str = "gender_based",
                                    provider: str = "google",
                                    custom_voices: Optional[Dict[str, List[str]]] = None) -> Dict[str, Dict]:
    """
    Get voice configuration for all speakers in a conversation.
    
    Args:
        speakers: List of speaker dictionaries
        voice_mode: Voice selection mode
        provider: TTS provider name
        custom_voices: Custom voice pool configuration
    
    Returns:
        Dictionary mapping speaker names to voice configurations
    """
    voice_manager = create_voice_manager(voice_mode, provider, custom_voices)
    voice_configs = {}
    
    for speaker in speakers:
        speaker_name = speaker["name"]
        gender = speaker["gender"]
        voice_config = voice_manager.get_voice_for_speaker(speaker_name, gender, provider)
        voice_configs[speaker_name] = voice_config
    
    return voice_configs
