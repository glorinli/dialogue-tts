#!/usr/bin/env python3
"""
Dialogue TTS Tool
Generates voice files for conversations with timing information.
"""

import os
from typing import Dict, List
from providers.registry import TTSProviderFactory
from utils.conversation_parser import (
    parse_conversation_content, 
    validate_conversation_data, 
    extract_speaker_mapping, 
    get_dialog_id
)
from utils.audio_utils import (
    get_audio_duration, 
    save_audio_file, 
    merge_audio_files, 
    ensure_directory_exists
)
from utils.file_utils import (
    save_json_output, 
    generate_unique_id, 
    create_dialogue_directory_structure,
    format_output_data,
    ensure_output_directory
)
from utils.unified_voice_manager import (
    create_unified_voice_manager,
    get_voice_config_for_conversation
)
from utils.multi_provider_tts import create_multi_provider_tts_manager


class DialogueTTS:
    def __init__(self, output_dir: str = "output", tts_provider: str = "google", 
                 voice_mode: str = "gender_based", custom_voices: dict = None, **tts_kwargs):
        self.output_dir = output_dir
        ensure_output_directory(output_dir)
        
        # Store provider name (legacy support)
        self.provider_name = tts_provider
        
        # Initialize multi-provider TTS manager first
        self.tts_manager = create_multi_provider_tts_manager(output_dir)
        
        # Initialize unified voice manager with available providers
        available_providers = self.tts_manager.get_available_providers()
        self.voice_manager = create_unified_voice_manager(voice_mode, available_providers)
        self.voice_mode = voice_mode
    
    def parse_conversation(self, content: str) -> List[Dict]:
        """Parse conversation content into individual dialogue lines."""
        return parse_conversation_content(content)
    
    def generate_speech(self, text: str, speaker_name: str, gender: str) -> str:
        """Generate speech from text using the appropriate TTS provider based on voice selection."""
        # Get voice configuration for this speaker (includes provider info)
        voice_config = self.voice_manager.get_voice_for_speaker(speaker_name, gender)
        
        # Generate speech using the multi-provider TTS manager
        return self.tts_manager.generate_speech(text, voice_config)
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file in seconds using pydub."""
        return get_audio_duration(audio_path)
    
    def save_audio_file(self, temp_mp3_path: str, output_filename: str, target_dir: str = None) -> str:
        """Save MP3 file with final filename."""
        if target_dir is None:
            target_dir = self.output_dir
        return save_audio_file(temp_mp3_path, output_filename, target_dir)
    
    def process_conversation(self, conversation_data: Dict) -> Dict:
        """Process conversation and generate voice files."""
        speakers = extract_speaker_mapping(conversation_data["speakers"])
        content = conversation_data["content"]
        
        # Get dialog ID from conversation data, generate if not provided
        dialog_id = get_dialog_id(conversation_data)
        if not dialog_id:
            # Fallback: generate unique dialog ID if not provided
            dialog_id = generate_unique_id()
            print(f"Warning: No dialog_id provided, generated: {dialog_id}")
        
        # Parse conversation lines
        dialogue_lines = self.parse_conversation(content)
        
        # Create dialogue-specific directory structure
        dialogue_dir, dialogue_audio_dir = create_dialogue_directory_structure(self.output_dir, dialog_id)
        
        current_time = 0.0
        
        for line in dialogue_lines:
            speaker_name = line["speaker"]
            text = line["text"]
            
            # Get speaker info
            speaker_info = speakers.get(speaker_name, {"gender": "unknown"})
            gender = speaker_info["gender"]
            
            # Generate speech
            temp_audio_path = self.generate_speech(text, speaker_name, gender)
            if temp_audio_path:
                # Get duration
                duration = self.get_audio_duration(temp_audio_path)
                
                # Update line info
                line["start_time"] = current_time
                line["duration"] = duration
                line["audio_file"] = f"{dialog_id}_{line['index']}.mp3"
                
                # Save audio file with final filename in dialogue audio directory
                final_audio_path = self.save_audio_file(temp_audio_path, line["audio_file"], dialogue_audio_dir)
                if final_audio_path:
                    current_time += duration
                else:
                    print(f"Failed to save audio for line {line['index']}")
            else:
                print(f"Failed to generate speech for line {line['index']}")
        
        # Create output structure
        output = format_output_data(
            dialog_id=dialog_id,
            speakers=conversation_data["speakers"],
            lines=dialogue_lines,
            total_duration=current_time,
            output_directory=dialogue_dir
        )
        
        # Merge individual audio files into a single output.mp3
        merged_audio_path = merge_audio_files(dialogue_audio_dir, dialog_id, dialogue_dir)
        if merged_audio_path:
            output["merged_audio_file"] = "output.mp3"
        
        return output
    
    def save_output(self, output_data: Dict, filename: str = None):
        """Save output JSON to file."""
        if filename is None:
            filename = "output.json"
        
        # Save to the dialogue-specific directory
        dialogue_dir = output_data.get("output_directory", self.output_dir)
        output_path = os.path.join(dialogue_dir, filename)
        
        success = save_json_output(output_data, output_path)
        return output_path if success else None
    
    def get_tts_provider_info(self) -> Dict:
        """Get information about the TTS providers and voice configuration."""
        return {
            "provider_name": "Multi-Provider",  # Now supports multiple providers
            "available_providers": self.tts_manager.get_available_providers(),
            "voice_mode": self.voice_mode,
            "voice_manager": self.voice_manager.mode.value,
            "voice_summary": self.voice_manager.get_available_voices_summary()
        }
    

    

    
    def get_voice_info_for_speaker(self, speaker_name: str, gender: str) -> Dict:
        """Get detailed voice information for a specific speaker."""
        return self.voice_manager.get_voice_for_speaker(speaker_name, gender)
    
    def set_voice_mode(self, mode: str):
        """Change the voice selection mode."""
        try:
            self.voice_manager = create_unified_voice_manager(mode)
            self.voice_mode = mode
            print(f"Voice mode changed to: {mode}")
        except ValueError:
            print(f"Invalid voice mode: {mode}. Available modes: fixed, random, gender_based")
    

    
    @staticmethod
    def get_available_providers() -> list:
        """Get list of available TTS providers."""
        return TTSProviderFactory.get_supported_providers()


def main():
    """Main function to demonstrate usage."""
    # Example conversation data
    conversation = {
        "dialog_id": "demo_conversation",
        "speakers": [
            {
                "name": "Jane",
                "gender": "female"
            },
            {
                "name": "David",
                "gender": "male"
            }
        ],
        "content": "Jane: Hi, David: Hello"
    }
    
    # Initialize TTS tool with voice management
    print("Available TTS providers:", DialogueTTS.get_available_providers())
    
    # Example 1: Gender-based voice selection (default)
    print("\n=== Example 1: Gender-based voices ===")
    tts_tool = DialogueTTS(voice_mode="gender_based")
    
    # Show voice information for speakers
    for speaker in conversation["speakers"]:
        voice_info = tts_tool.get_voice_info_for_speaker(speaker["name"], speaker["gender"])
        print(f"Speaker {speaker['name']} ({speaker['gender']}): {voice_info['voice_name']}")
    
    # Process conversation
    output = tts_tool.process_conversation(conversation)
    tts_tool.save_output(output)
    
    # Example 2: Fixed voices (same speaker always gets same voice)
    print("\n=== Example 2: Fixed voices ===")
    tts_tool_fixed = DialogueTTS(voice_mode="fixed")
    
    # Show voice assignments
    for speaker in conversation["speakers"]:
        voice_info = tts_tool_fixed.get_voice_info_for_speaker(speaker["name"], speaker["gender"])
        print(f"Speaker {speaker['name']} ({speaker['gender']}): {voice_info['voice_name']} (fixed)")
    
    # Example 3: Random voices
    print("\n=== Example 3: Random voices ===")
    tts_tool_random = DialogueTTS(voice_mode="random")
    
    # Show random voice assignments
    for speaker in conversation["speakers"]:
        voice_info = tts_tool_random.get_voice_info_for_speaker(speaker["name"], speaker["gender"])
        print(f"Speaker {speaker['name']} ({speaker['gender']}): {voice_info['voice_name']} (random)")
    
    print(f"\nGenerated {len(output['lines'])} audio files")
    print(f"Total duration: {output['total_duration']:.2f} seconds")
    print(f"Output directory: {output['output_directory']}")
    if "merged_audio_file" in output:
        print(f"Merged audio: {os.path.join(output['output_directory'], output['merged_audio_file'])}")


if __name__ == "__main__":
    main()
