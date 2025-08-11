# Dialogue TTS Tool

A Python tool to generate voice files for conversations with timing information.

## Features

- Generate voice files from conversation text using multiple TTS providers
- Currently supports Google Text-to-Speech (gTTS) with extensible architecture
- **Advanced voice management** with three selection modes:
  - **Fixed**: Each speaker gets a consistent voice across conversations
  - **Random**: Random voice selection for each speaker
  - **Gender-based**: Standard gender-appropriate voices
- Support for multiple speakers with gender-based voice selection
- Automatic parsing of conversation format
- JSON output with timing information (start time, duration, index)
- MP3 audio file generation with organized naming
- Easy to add new TTS providers (Azure, AWS Polly, OpenAI, etc.)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. No additional audio processing tools required - MP3 files are generated directly

## Usage

### Command Line Usage

The main script supports both single file and batch processing:

```bash
# Process a single conversation file
python main.py conversation.json

# Process all JSON files in a directory
python main.py conversations/

# Specify output directory and TTS settings
python main.py conversation.json --output my_output --provider google --lang en

# Use different voice selection modes
python main.py conversation.json --voice-mode fixed    # Consistent voices per speaker
python main.py conversation.json --voice-mode random   # Random voice selection
python main.py conversation.json --voice-mode gender_based  # Gender-appropriate voices
```

### Programmatic Usage

```python
from dialogue_tts import DialogueTTS

# Initialize with different voice modes
tts_tool = DialogueTTS(output_dir="my_conversations", voice_mode="gender_based")  # Default
tts_tool = DialogueTTS(output_dir="my_conversations", voice_mode="fixed")         # Consistent voices
tts_tool = DialogueTTS(output_dir="my_conversations", voice_mode="random")        # Random voices

# Or specify a different provider
tts_tool = DialogueTTS(output_dir="my_conversations", tts_provider="google", lang="en")

# Voice management features
tts_tool.set_voice_mode("fixed")                    # Change voice mode
tts_tool.add_custom_voice("female", "custom-voice") # Add custom voice
tts_tool.clear_voice_cache()                        # Clear voice assignments

# Define your conversation
conversation = {
    "speakers": [
        {"name": "Jane", "gender": "female"},
        {"name": "David", "gender": "male"}
    ],
    "content": "Jane: Hi, David: Hello"
}

# Process conversation
output = tts_tool.process_conversation(conversation)

# Save output
tts_tool.save_output(output)
```

### Conversation Format

The conversation should follow this JSON structure:

```json
{
    "dialog_id": "unique_dialogue_identifier",
    "speakers": [
        {
            "name": "SpeakerName",
            "gender": "female|male"
        }
    ],
    "content": "Speaker1: Text here, Speaker2: More text here"
}
```

**Note**: The `dialog_id` field is used to name the output folder. If not provided, a unique ID will be generated automatically.

### Output

The tool generates a separate folder for each dialogue with the following structure:

```
output/
└── unique_dialogue_identifier/     # Uses dialog_id from JSON
    ├── output.json                 # Conversation metadata and timing information
    ├── output.mp3                  # Merged audio file (entire conversation)
    └── audio/
        ├── unique_dialogue_identifier_0.mp3
        ├── unique_dialogue_identifier_1.mp3
        └── ...
```

Example JSON output:
```json
{
    "dialog_id": "unique_dialogue_identifier",
    "speakers": [...],
    "total_duration": 5.23,
    "merged_audio_file": "output.mp3",
    "lines": [
        {
            "index": 0,
            "speaker": "Jane",
            "text": "Hi",
            "start_time": 0.0,
            "duration": 1.2,
            "audio_file": "unique_dialogue_identifier_0.mp3"
        }
    ]
}
```

## Running Examples

```bash
# Run basic example
python dialogue_tts.py

# Process a single conversation file
python main.py examples/conversation1.json

# Process all conversations in a directory
python main.py examples/

# Process with custom settings
python main.py examples/ --output my_conversations --lang en
```

## File Structure

```
dialogue-tts/
├── dialogue_tts.py      # Main TTS tool
├── tts_providers.py     # TTS provider abstractions
├── main.py             # Command-line interface for batch processing
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── utils/              # Utility modules
│   ├── __init__.py
│   ├── conversation_parser.py  # Conversation parsing and validation
│   ├── audio_utils.py          # Audio processing utilities
│   └── file_utils.py           # File operations and output management
├── examples/           # Example conversation files
│   ├── conversation1.json
│   ├── conversation2.json
│   └── conversation3.json
└── output/             # Generated files (created automatically)
    └── unique_dialogue_identifier/     # Uses dialog_id from JSON
        ├── output.json                 # Conversation metadata
        ├── output.mp3                  # Merged audio file
        └── audio/                      # Individual MP3 audio files
            ├── unique_dialogue_identifier_0.mp3
            ├── unique_dialogue_identifier_1.mp3
            └── ...
```

## Dependencies

- `gTTS`: Google Text-to-Speech API (default provider)
- `pydub`: Audio processing and merging
- `requests`: HTTP requests
- `python-dotenv`: Environment variable management

## Architecture

The tool uses a provider-based architecture:

- **`TTSProvider`**: Abstract base class defining the interface for TTS services
- **`GoogleTTSProvider`**: Implementation using Google TTS
- **`TTSProviderFactory`**: Factory class for creating and managing TTS providers
- **`DialogueTTS`**: Main class that orchestrates the conversation processing

### Adding New TTS Providers

To add a new TTS provider (e.g., Azure, AWS Polly):

1. Create a new class inheriting from `TTSProvider`
2. Implement the required abstract methods
3. Register it with the factory:

```python
from tts_providers import TTSProviderFactory

class MyCustomTTSProvider(TTSProvider):
    # Implement required methods...
    pass

# Register the provider
TTSProviderFactory.register_provider("my_custom", MyCustomTTSProvider)
```

## Notes

- Requires internet connection for gTTS
- Audio files are generated in MP3 format
- Each conversation gets a unique dialog ID based on timestamp
- Temporary MP3 files are automatically renamed to final filenames
- Individual audio files are merged into a single `output.mp3` file
- Requires ffmpeg for audio processing (installed automatically with pydub)
