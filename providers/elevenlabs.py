#!/usr/bin/env python3
"""
ElevenLabs TTS Provider
Uses ElevenLabs AI voice generation for high-quality speech.
"""

import os
import uuid
from datetime import datetime
from typing import Dict, Optional
from elevenlabs import client
from .base import TTSProvider


class ElevenLabsTTSProvider(TTSProvider):
    """ElevenLabs Text-to-Speech provider."""
    
    def __init__(self, output_dir: str, api_key: str = None, **kwargs):
        """
        Initialize ElevenLabs TTS provider.
        
        Args:
            output_dir: Directory to save generated audio files
            api_key: ElevenLabs API key (optional, will try to load from .env)
            **kwargs: Additional arguments (ignored for ElevenLabs)
        """
        self.output_dir = output_dir
        
        # Get API key from parameter or environment variable
        if api_key:
            self.api_key = api_key
        else:
            # Try to load from environment
            from dotenv import load_dotenv
            load_dotenv()
            self.api_key = os.getenv('ELEVENLABS_API_KEY')
            if not self.api_key:
                raise ValueError("ElevenLabs API key not provided. Set ELEVENLABS_API_KEY in .env file or pass api_key parameter.")
        
        # Initialize ElevenLabs client
        self.client = client.ElevenLabs(api_key=self.api_key)
    
    def _get_voice_id(self, voice_config: Dict) -> str:
        """
        Get voice ID from voice configuration.
        
        Args:
            voice_config: Voice configuration dictionary from unified_voices.json
            
        Returns:
            Voice ID string
        """
        # Get voice_id directly from the config
        voice_id = voice_config.get('voice_id')
        if not voice_id:
            raise ValueError("voice_id not found in voice configuration")
        return voice_id
    
    def generate_speech(self, text: str, speaker_name: str, gender: str, **kwargs) -> Optional[str]:
        """
        Generate speech using ElevenLabs TTS.
        
        Args:
            text: Text to convert to speech
            speaker_name: Name of the speaker
            gender: Gender of the speaker ('male' or 'female')
            **kwargs: Additional arguments including voice_config
            
        Returns:
            Path to the generated audio file, or None if generation failed
        """
        try:
            # Get voice configuration
            voice_config = kwargs.get('voice_config', {})
            
            # Get voice ID from config
            voice_id = self._get_voice_id(voice_config)
            
            # Generate speech using client
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_monolingual_v1"
            )
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"temp_{timestamp}_{speaker_name}_{uuid.uuid4().hex[:8]}.mp3"
            temp_path = os.path.join(self.output_dir, filename)
            
            # Save audio by writing bytes to file
            with open(temp_path, 'wb') as f:
                for chunk in audio:
                    f.write(chunk)
            
            return temp_path
            
        except Exception as e:
            print(f"Error generating speech with ElevenLabs TTS for '{text}': {e}")
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
        return ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh']
    
    def get_supported_voices(self) -> Dict:
        """
        Get dictionary of available voices.
        
        Returns:
            Dictionary mapping voice names to voice information
        """
        # Return empty dict since we don't need to fetch voices from API
        # Voice information is managed by the unified voice manager
        return {}
