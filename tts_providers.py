#!/usr/bin/env python3
"""
TTS Provider Abstractions
Supports multiple text-to-speech services with a common interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from gtts import gTTS
import os


class TTSProvider(ABC):
    """Abstract base class for TTS providers."""
    
    @abstractmethod
    def generate_speech(self, text: str, speaker_name: str, gender: str, **kwargs) -> Optional[str]:
        """Generate speech from text and return the audio file path."""
        pass
    
    @abstractmethod
    def get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file in seconds."""
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> list:
        """Get list of supported languages."""
        pass
    
    @abstractmethod
    def get_supported_voices(self) -> Dict:
        """Get dictionary of supported voices."""
        pass


class GoogleTTSProvider(TTSProvider):
    """Google Text-to-Speech provider using gTTS."""
    
    def __init__(self, output_dir: str, lang: str = 'en', tld: str = 'com'):
        self.output_dir = output_dir
        self.lang = lang
        self.tld = tld
        self.supported_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh']
    
    def generate_speech(self, text: str, speaker_name: str, gender: str, **kwargs) -> Optional[str]:
        """Generate speech using Google TTS."""
        try:
            # Override language if specified in kwargs
            lang = kwargs.get('lang', self.lang)
            tld = kwargs.get('tld', self.tld)
            
            # Create TTS object
            tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
            
            # Generate unique filename
            import uuid
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"temp_{timestamp}_{speaker_name}_{uuid.uuid4().hex[:8]}.mp3"
            temp_path = os.path.join(self.output_dir, filename)
            
            # Save audio
            tts.save(temp_path)
            
            return temp_path
        except Exception as e:
            print(f"Error generating speech with Google TTS for '{text}': {e}")
            return None
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Get duration using pydub (handled by DialogueTTS class)."""
        # This method is kept for interface compatibility
        # Actual duration calculation is now handled by DialogueTTS.get_audio_duration()
        return 2.0  # Default fallback
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages."""
        return self.supported_languages
    
    def get_supported_voices(self) -> Dict:
        """Get dictionary of supported voices."""
        return {
            'en': {'male': 'en', 'female': 'en'},
            'es': {'male': 'es', 'female': 'es'},
            'fr': {'male': 'fr', 'female': 'fr'},
            'de': {'male': 'de', 'female': 'de'},
            'it': {'male': 'it', 'female': 'it'},
            'pt': {'male': 'pt', 'female': 'pt'},
            'ru': {'male': 'ru', 'female': 'ru'},
            'ja': {'male': 'ja', 'female': 'ja'},
            'ko': {'male': 'ko', 'female': 'ko'},
            'zh': {'male': 'zh', 'female': 'zh'}
        }


class TTSProviderFactory:
    """Factory class for creating TTS providers."""
    
    _providers = {
        'google': GoogleTTSProvider,
        # Future providers can be added here:
        # 'azure': AzureTTSProvider,
        # 'aws': AWSPollyProvider,
        # 'openai': OpenAITTSProvider,
    }
    
    @classmethod
    def create_provider(cls, provider_name: str, output_dir: str, **kwargs) -> TTSProvider:
        """Create a TTS provider instance."""
        if provider_name not in cls._providers:
            raise ValueError(f"Unsupported TTS provider: {provider_name}. "
                           f"Supported providers: {list(cls._providers.keys())}")
        
        provider_class = cls._providers[provider_name]
        return provider_class(output_dir, **kwargs)
    
    @classmethod
    def get_supported_providers(cls) -> list:
        """Get list of supported provider names."""
        return list(cls._providers.keys())
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """Register a new TTS provider."""
        if not issubclass(provider_class, TTSProvider):
            raise ValueError("Provider class must inherit from TTSProvider")
        cls._providers[name] = provider_class
