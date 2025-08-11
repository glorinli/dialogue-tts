#!/usr/bin/env python3
"""
Base TTS Provider Interface
Defines the common interface that all TTS providers must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional


class TTSProvider(ABC):
    """Abstract base class for TTS providers."""
    
    @abstractmethod
    def generate_speech(self, text: str, speaker_name: str, gender: str, **kwargs) -> Optional[str]:
        """
        Generate speech from text and return the audio file path.
        
        Args:
            text: Text to convert to speech
            speaker_name: Name of the speaker
            gender: Gender of the speaker ('male' or 'female')
            **kwargs: Additional provider-specific arguments
            
        Returns:
            Path to the generated audio file, or None if generation failed
        """
        pass
    
    @abstractmethod
    def get_audio_duration(self, audio_path: str) -> float:
        """
        Get duration of audio file in seconds.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Duration in seconds
        """
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> list:
        """
        Get list of supported languages.
        
        Returns:
            List of supported language codes
        """
        pass
    
    @abstractmethod
    def get_supported_voices(self) -> Dict:
        """
        Get dictionary of supported voices.
        
        Returns:
            Dictionary mapping voice names to voice information
        """
        pass
