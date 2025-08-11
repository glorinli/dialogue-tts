#!/usr/bin/env python3
"""
Dialogue TTS Tool
Generates voice files for conversations with timing information.
"""

from typing import Dict, List
from tts_providers import TTSProviderFactory, TTSProvider
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


class DialogueTTS:
    def __init__(self, output_dir: str = "output", tts_provider: str = "google", **tts_kwargs):
        self.output_dir = output_dir
        ensure_output_directory(output_dir)
        
        # Initialize TTS provider
        self.tts_provider = TTSProviderFactory.create_provider(
            tts_provider, output_dir, **tts_kwargs
        )
    
    def parse_conversation(self, content: str) -> List[Dict]:
        """Parse conversation content into individual dialogue lines."""
        return parse_conversation_content(content)
    
    def generate_speech(self, text: str, speaker_name: str, gender: str) -> str:
        """Generate speech from text using the configured TTS provider."""
        return self.tts_provider.generate_speech(text, speaker_name, gender)
    
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
        """Get information about the current TTS provider."""
        return {
            "provider_name": self.tts_provider.__class__.__name__,
            "supported_languages": self.tts_provider.get_supported_languages(),
            "supported_voices": self.tts_provider.get_supported_voices()
        }
    
    def change_tts_provider(self, provider_name: str, **kwargs):
        """Change the TTS provider."""
        self.tts_provider = TTSProviderFactory.create_provider(
            provider_name, self.audio_dir, **kwargs
        )
        print(f"Changed TTS provider to: {provider_name}")
    

    
    @staticmethod
    def get_available_providers() -> list:
        """Get list of available TTS providers."""
        return TTSProviderFactory.get_supported_providers()


def main():
    """Main function to demonstrate usage."""
    # Example conversation data
    conversation = {
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
    
    # Initialize TTS tool with default Google TTS provider
    print("Available TTS providers:", DialogueTTS.get_available_providers())
    tts_tool = DialogueTTS()
    
    # Show provider information
    provider_info = tts_tool.get_tts_provider_info()
    print(f"Using TTS provider: {provider_info['provider_name']}")
    print(f"Supported languages: {provider_info['supported_languages']}")
    
    # Process conversation
    print("\nProcessing conversation...")
    output = tts_tool.process_conversation(conversation)
    
    # Save output
    tts_tool.save_output(output)
    
    print(f"Generated {len(output['lines'])} audio files")
    print(f"Total duration: {output['total_duration']:.2f} seconds")
    print(f"Output directory: {output['output_directory']}")
    print(f"Audio files location: {os.path.join(output['output_directory'], 'audio')}")
    if "merged_audio_file" in output:
        print(f"Merged audio: {os.path.join(output['output_directory'], output['merged_audio_file'])}")


if __name__ == "__main__":
    main()
