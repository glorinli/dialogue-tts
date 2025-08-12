#!/usr/bin/env python3
"""
Multi-Provider TTS Manager
Handles TTS generation across multiple providers in a single conversation.
"""

import os
from typing import Dict, Any, Optional
from providers.registry import TTSProviderFactory


class MultiProviderTTSManager:
    """Manages TTS generation across multiple providers."""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.providers = {}  # Cache for provider instances
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available TTS providers."""
        available_providers = TTSProviderFactory.get_supported_providers()
        
        for provider_name in available_providers:
            try:
                # Create provider instance (without API key for now)
                provider = TTSProviderFactory.create_provider(provider_name, self.output_dir)
                self.providers[provider_name] = provider
            except Exception as e:
                print(f"Warning: Could not initialize {provider_name} provider: {e}")
    
    def generate_speech(self, text: str, voice_config: Dict[str, Any]) -> Optional[str]:
        """
        Generate speech using the appropriate provider based on voice configuration.
        
        Args:
            text: Text to convert to speech
            voice_config: Voice configuration including provider info
            
        Returns:
            Path to the generated audio file, or None if generation failed
        """
        provider_name = voice_config.get('provider')
        if not provider_name:
            raise ValueError("Voice configuration must include 'provider' field")
        
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not available or not initialized")
        
        provider = self.providers[provider_name]
        
        try:
            # Generate speech using the appropriate provider
            # Extract speaker info from voice config for compatibility
            speaker_name = voice_config.get('voice_name', 'unknown')
            gender = voice_config.get('gender', 'unknown')
            
            # Call the provider's generate_speech method with the expected signature
            return provider.generate_speech(text, speaker_name, gender, voice_config=voice_config)
        except Exception as e:
            print(f"Error generating speech with {provider_name}: {e}")
            return None
    
    def get_provider_info(self, provider_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific provider."""
        if provider_name not in self.providers:
            return None
        
        provider = self.providers[provider_name]
        return {
            'name': provider_name,
            'class': provider.__class__.__name__,
            'output_dir': getattr(provider, 'output_dir', 'Unknown')
        }
    
    def get_available_providers(self) -> list:
        """Get list of available and initialized providers."""
        return list(self.providers.keys())
    
    def test_provider(self, provider_name: str) -> bool:
        """Test if a provider is working correctly."""
        if provider_name not in self.providers:
            return False
        
        try:
            provider = self.providers[provider_name]
            # Try to get provider info to test basic functionality
            info = self.get_provider_info(provider_name)
            return info is not None
        except Exception:
            return False


def create_multi_provider_tts_manager(output_dir: str) -> MultiProviderTTSManager:
    """
    Create a multi-provider TTS manager instance.
    
    Args:
        output_dir: Directory to save generated audio files
    
    Returns:
        Configured MultiProviderTTSManager instance
    """
    return MultiProviderTTSManager(output_dir)
