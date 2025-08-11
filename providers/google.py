#!/usr/bin/env python3
"""
Google TTS Provider
Uses Google Text-to-Speech (gTTS) for speech generation.
"""

import os
import uuid
from datetime import datetime
from typing import Dict, Optional
from gtts import gTTS
from .base import TTSProvider


class GoogleTTSProvider(TTSProvider):
    """Google Text-to-Speech provider using gTTS."""
    
    def __init__(self, output_dir: str, lang: str = 'en', tld: str = 'com'):
        """
        Initialize Google TTS provider.
        
        Args:
            output_dir: Directory to save generated audio files
            lang: Language code (default: 'en')
            tld: Top-level domain for Google TTS (default: 'com')
        """
        self.output_dir = output_dir
        self.lang = lang
        self.tld = tld
        self.supported_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh']
    
    def generate_speech(self, text: str, speaker_name: str, gender: str, **kwargs) -> Optional[str]:
        """
        Generate speech using Google TTS.
        
        Args:
            text: Text to convert to speech
            speaker_name: Name of the speaker
            gender: Gender of the speaker ('male' or 'female')
            **kwargs: Additional arguments including voice_config
            
        Returns:
            Path to the generated audio file, or None if generation failed
        """
        try:
            # Handle voice configuration
            voice_config = kwargs.get('voice_config', {})
            voice_name = voice_config.get('voice_name', 'default')
            
            # Get TLD directly from voice configuration
            if voice_config.get('tld'):
                tld = voice_config.get('tld')
            else:
                tld = self.tld
            
            # Create TTS object
            tts = gTTS(text=text, lang=self.lang, tld=tld, slow=False)
            
            # Generate unique filename
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
        """
        Get duration using pydub (handled by DialogueTTS class).
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Default duration (actual calculation handled by DialogueTTS)
        """
        # This method is kept for interface compatibility
        # Actual duration calculation is now handled by DialogueTTS.get_audio_duration()
        return 2.0  # Default fallback
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported languages.
        
        Returns:
            List of supported language codes
        """
        return self.supported_languages
    
    def get_supported_voices(self) -> Dict:
        """
        Get dictionary of supported voices.
        
        Returns:
            Dictionary mapping languages to voice information
        """
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
