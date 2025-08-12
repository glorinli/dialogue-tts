#!/usr/bin/env python3
"""
Unified Voice Management
Handles voice selection across multiple TTS providers in a single conversation.
"""

import json
import os
import random
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum


class VoiceSelectionMode(Enum):
    """Voice selection modes."""
    FIXED = "fixed"      # Use specific voice for each speaker
    RANDOM = "random"    # Randomly select from available voices
    GENDER_BASED = "gender_based"  # Select based on gender only


class UnifiedVoiceManager:
    """Manages voice selection across multiple TTS providers."""
    
    def __init__(self, mode: VoiceSelectionMode = VoiceSelectionMode.GENDER_BASED, available_providers: list = None):
        self.mode = mode
        self.voice_cache = {}  # Cache for fixed voice assignments
        self.available_voices = self._initialize_voice_pool()
        self.provider_weights = self._load_provider_weights()
        
        # Filter voices to only include available providers
        if available_providers:
            self._filter_voices_by_available_providers(available_providers)
    
    def _initialize_voice_pool(self) -> Dict[str, List[Dict]]:
        """Initialize the pool of available voices by gender from unified config."""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'providers', 'configs', 'unified_voices.json')
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                voices = config.get('voices', {})
                if not voices:
                    raise ValueError("No voices found in unified_voices.json")
                return voices
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load unified voice configuration: {e}")
    
    def _load_provider_weights(self) -> Dict[str, float]:
        """Load provider weights for balanced selection."""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'providers', 'configs', 'unified_voices.json')
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get('provider_weights', {'google': 0.5, 'elevenlabs': 0.5})
        except (FileNotFoundError, json.JSONDecodeError):
            return {'google': 0.5, 'elevenlabs': 0.5}
    
    def get_voice_for_speaker(self, speaker_name: str, gender: str) -> Dict[str, Any]:
        """
        Get voice configuration for a speaker.
        
        Args:
            speaker_name: Name of the speaker
            gender: Gender of the speaker ('male' or 'female')
        
        Returns:
            Dictionary with voice configuration including provider info
        """
        if self.mode == VoiceSelectionMode.FIXED:
            return self._get_fixed_voice(speaker_name, gender)
        elif self.mode == VoiceSelectionMode.RANDOM:
            return self._get_random_voice(gender)
        else:  # GENDER_BASED
            return self._get_gender_based_voice(gender)
    
    def _get_fixed_voice(self, speaker_name: str, gender: str) -> Dict[str, Any]:
        """Get or assign a fixed voice for a speaker."""
        cache_key = f"{speaker_name}_{gender}"
        
        if cache_key not in self.voice_cache:
            # Assign a new voice for this speaker
            available_voices = self.available_voices.get(gender, [])
            if available_voices:
                selected_voice = random.choice(available_voices)
                self.voice_cache[cache_key] = selected_voice
            else:
                raise ValueError(f"No voices available for gender '{gender}'. "
                               f"Please check the unified voice configuration.")
        
        cached_voice = self.voice_cache[cache_key]
        return self._format_voice_config(cached_voice, gender, "fixed")
    
    def _get_random_voice(self, gender: str) -> Dict[str, Any]:
        """Get a random voice for the specified gender."""
        available_voices = self.available_voices.get(gender, [])
        if not available_voices:
            raise ValueError(f"No voices available for gender '{gender}'. "
                           f"Please check the unified voice configuration.")
        
        selected_voice = random.choice(available_voices)
        return self._format_voice_config(selected_voice, gender, "random")
    
    def _get_gender_based_voice(self, gender: str) -> Dict[str, Any]:
        """Get a voice based on gender with provider balancing."""
        available_voices = self.available_voices.get(gender, [])
        if not available_voices:
            raise ValueError(f"No voices available for gender '{gender}'. "
                           f"Please check the unified voice configuration.")
        
        # Use weighted random selection to balance providers
        selected_voice = self._select_weighted_voice(available_voices)
        return self._format_voice_config(selected_voice, gender, "gender_based")
    
    def _select_weighted_voice(self, voices: List[Dict]) -> Dict:
        """Select a voice using provider weights for balanced distribution."""
        # Group voices by provider
        provider_voices = {}
        for voice in voices:
            provider = voice.get('provider', 'google')
            if provider not in provider_voices:
                provider_voices[provider] = []
            provider_voices[provider].append(voice)
        
        # Select provider based on weights
        providers = list(self.provider_weights.keys())
        weights = [self.provider_weights.get(p, 0.1) for p in providers]
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        else:
            weights = [1.0 / len(providers)] * len(providers)
        
        selected_provider = random.choices(providers, weights=weights)[0]
        
        # Select random voice from the chosen provider
        if selected_provider in provider_voices:
            return random.choice(provider_voices[selected_provider])
        else:
            # Fallback to random selection if provider has no voices
            return random.choice(voices)
    
    def _format_voice_config(self, voice: Dict, gender: str, mode: str) -> Dict[str, Any]:
        """Format voice configuration for consistent output."""
        config = {
            "voice_name": voice["name"],
            "gender": gender,
            "provider": voice["provider"],
            "mode": mode
        }
        
        # Add provider-specific fields
        if voice["provider"] == "google":
            config["tld"] = voice.get("tld", "com")
        elif voice["provider"] == "elevenlabs":
            config["voice_id"] = voice.get("voice_id")
        
        return config
    
    def get_available_voices_summary(self) -> Dict[str, Any]:
        """Get summary of available voices by gender and provider."""
        summary = {}
        
        for gender, voices in self.available_voices.items():
            summary[gender] = {
                "total": len(voices),
                "providers": {}
            }
            
            # Count voices by provider
            for voice in voices:
                provider = voice.get("provider", "unknown")
                if provider not in summary[gender]["providers"]:
                    summary[gender]["providers"][provider] = 0
                summary[gender]["providers"][provider] += 1
        
        return summary
    
    def get_voice_by_name(self, voice_name: str) -> Optional[Dict[str, Any]]:
        """Get voice configuration by name."""
        for gender, voices in self.available_voices.items():
            for voice in voices:
                if voice.get("name") == voice_name:
                    return self._format_voice_config(voice, gender, "fixed")
        return None
    
    def _filter_voices_by_available_providers(self, available_providers: list):
        """Filter voices to only include those from available providers."""
        for gender in self.available_voices:
            self.available_voices[gender] = [
                voice for voice in self.available_voices[gender]
                if voice.get('provider') in available_providers
            ]
        
        # Update provider weights to only include available providers
        self.provider_weights = {
            provider: weight for provider, weight in self.provider_weights.items()
            if provider in available_providers
        }


def create_unified_voice_manager(mode: str = "gender_based", available_providers: list = None) -> UnifiedVoiceManager:
    """
    Create a unified voice manager instance.
    
    Args:
        mode: Voice selection mode ('fixed', 'random', 'gender_based')
        available_providers: List of available TTS providers to filter voices
    
    Returns:
        Configured UnifiedVoiceManager instance
    """
    mode_enum = VoiceSelectionMode(mode)
    return UnifiedVoiceManager(mode_enum, available_providers)


def get_voice_config_for_conversation(conversation_data: Dict, mode: str = "gender_based") -> Dict[str, Any]:
    """
    Get voice configuration for an entire conversation.
    
    Args:
        conversation_data: Conversation data dictionary
        mode: Voice selection mode
    
    Returns:
        Dictionary mapping speaker names to voice configurations
    """
    voice_manager = create_unified_voice_manager(mode)
    speakers = conversation_data.get("speakers", {})
    
    voice_configs = {}
    for speaker_name, speaker_info in speakers.items():
        gender = speaker_info.get("gender", "unknown")
        if gender in ["male", "female"]:
            voice_configs[speaker_name] = voice_manager.get_voice_for_speaker(speaker_name, gender)
    
    return voice_configs
