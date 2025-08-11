#!/usr/bin/env python3
"""
TTS Provider Factory
Creates and manages TTS provider instances.
"""

from typing import Dict, Type
from .base import TTSProvider


class TTSProviderFactory:
    """Factory class for creating TTS providers."""
    
    _providers: Dict[str, Type[TTSProvider]] = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[TTSProvider]):
        """
        Register a new TTS provider.
        
        Args:
            name: Provider name (e.g., 'google', 'elevenlabs')
            provider_class: Provider class that inherits from TTSProvider
        """
        if not issubclass(provider_class, TTSProvider):
            raise ValueError("Provider class must inherit from TTSProvider")
        cls._providers[name] = provider_class
    
    @classmethod
    def create_provider(cls, provider_name: str, output_dir: str, **kwargs) -> TTSProvider:
        """
        Create a TTS provider instance.
        
        Args:
            provider_name: Name of the provider to create
            output_dir: Directory to save generated audio files
            **kwargs: Additional provider-specific arguments
            
        Returns:
            Configured TTS provider instance
            
        Raises:
            ValueError: If provider name is not supported
        """
        if provider_name not in cls._providers:
            raise ValueError(f"Unsupported TTS provider: {provider_name}. "
                           f"Supported providers: {list(cls._providers.keys())}")
        
        provider_class = cls._providers[provider_name]
        return provider_class(output_dir, **kwargs)
    
    @classmethod
    def get_supported_providers(cls) -> list:
        """
        Get list of supported provider names.
        
        Returns:
            List of registered provider names
        """
        return list(cls._providers.keys())
    
    @classmethod
    def is_provider_supported(cls, provider_name: str) -> bool:
        """
        Check if a provider is supported.
        
        Args:
            provider_name: Name of the provider to check
            
        Returns:
            True if provider is supported, False otherwise
        """
        return provider_name in cls._providers
