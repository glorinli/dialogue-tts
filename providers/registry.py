#!/usr/bin/env python3
"""
Provider Registry
Automatically imports and registers all available TTS providers.
"""

from .factory import TTSProviderFactory
from .google import GoogleTTSProvider
from .elevenlabs import ElevenLabsTTSProvider

# Register all available providers
TTSProviderFactory.register_provider('google', GoogleTTSProvider)
TTSProviderFactory.register_provider('elevenlabs', ElevenLabsTTSProvider)

# List of all available providers
AVAILABLE_PROVIDERS = ['google', 'elevenlabs']
