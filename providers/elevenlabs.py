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
        
        # Cache available voices
        self._available_voices = None
        self._voice_cache = {}
    
    def _get_available_voices(self):
        """Get and cache available voices from ElevenLabs."""
        if self._available_voices is None:
            try:
                voices_response = self.client.voices.get_all()
                self._available_voices = voices_response.voices
            except Exception as e:
                print(f"Warning: Could not fetch ElevenLabs voices: {e}")
                self._available_voices = []
        return self._available_voices
    
    def _get_voice_for_gender(self, gender: str, voice_config: Dict) -> str:
        """
        Get voice ID for a specific gender.
        
        Args:
            gender: Gender of the speaker ('male' or 'female')
            voice_config: Voice configuration dictionary
            
        Returns:
            Voice ID string
        """
        # Check if voice_config specifies a voice name
        voice_name = voice_config.get('voice_name', '')
        
        # If we have a specific voice name, try to find it
        if voice_name and voice_name in self._voice_cache:
            return self._voice_cache[voice_name]
        
        # Get available voices
        available_voices = self._get_available_voices()
        
        # Filter by gender if specified
        gender_voices = []
        for voice in available_voices:
            # ElevenLabs doesn't have explicit gender, but we can use labels or names
            voice_labels = getattr(voice, 'labels', {}) or {}
            voice_name_lower = getattr(voice, 'name', '').lower()
            
            # Check if voice has gender label or name suggests gender
            if gender.lower() == 'male':
                if 'male' in voice_labels.get('gender', '').lower() or 'male' in voice_name_lower:
                    gender_voices.append(voice)
            elif gender.lower() == 'female':
                if 'female' in voice_labels.get('gender', '').lower() or 'female' in voice_name_lower:
                    gender_voices.append(voice)
        
        # If no gender-specific voices found, use all voices
        if not gender_voices:
            gender_voices = available_voices
        
        # Select first available voice
        if gender_voices:
            selected_voice = gender_voices[0]
            voice_id = getattr(selected_voice, 'voice_id', None)
            
            # Cache the voice name for future use
            if voice_name:
                self._voice_cache[voice_name] = voice_id
            
            return voice_id
        
        # Fallback to a default voice
        return "pNInz6obpgDQGcFmaJgB"  # Adam (male) as fallback
    
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
            
            # Get voice ID for this gender
            voice_id = self._get_voice_for_gender(gender, voice_config)
            
            # Generate speech
            audio = generate(
                text=text,
                voice=voice_id,
                model="eleven_monolingual_v1"
            )
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"temp_{timestamp}_{speaker_name}_{uuid.uuid4().hex[:8]}.mp3"
            temp_path = os.path.join(self.output_dir, filename)
            
            # Save audio
            save(audio, temp_path)
            
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
        try:
            available_voices = self._get_available_voices()
            voice_info = {}
            
            for voice in available_voices:
                voice_name = getattr(voice, 'name', 'Unknown')
                voice_id = getattr(voice, 'voice_id', 'Unknown')
                voice_info[voice_name] = {
                    'id': voice_id,
                    'name': voice_name,
                    'labels': getattr(voice, 'labels', {})
                }
            
            return voice_info
        except Exception as e:
            print(f"Warning: Could not get voice information: {e}")
            return {}
