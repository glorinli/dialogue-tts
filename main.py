#!/usr/bin/env python3
"""
Main script for processing dialogue TTS
Supports single file input and folder input with JSON files.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Union
from dialogue_tts import DialogueTTS
from utils.conversation_parser import validate_conversation_data


def load_conversation_from_file(file_path: str) -> Dict:
    """Load conversation data from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate required fields
        if 'speakers' not in data or 'content' not in data:
            raise ValueError(f"Invalid conversation format in {file_path}. "
                           f"Required fields: 'speakers', 'content'")
        
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file_path}: {e}")
    except Exception as e:
        raise ValueError(f"Error reading {file_path}: {e}")


def validate_conversation(data: Dict, file_path: str = None) -> bool:
    """Validate conversation data structure."""
    is_valid, error_message = validate_conversation_data(data)
    if not is_valid:
        if file_path:
            print(f"Validation error in {file_path}: {error_message}")
        else:
            print(f"Validation error: {error_message}")
    return is_valid


def find_json_files(input_path: str) -> List[str]:
    """Find all JSON files in the given path (file or directory)."""
    path = Path(input_path)
    
    if path.is_file():
        if path.suffix.lower() == '.json':
            return [str(path)]
        else:
            raise ValueError(f"File {input_path} is not a JSON file")
    
    elif path.is_dir():
        json_files = list(path.glob('*.json'))
        if not json_files:
            raise ValueError(f"No JSON files found in directory {input_path}")
        return [str(f) for f in json_files]
    
    else:
        raise ValueError(f"Path {input_path} does not exist")


def process_single_conversation(tts_tool: DialogueTTS, conversation_data: Dict, 
                              file_path: str = None) -> Dict:
    """Process a single conversation and return the output."""
    try:
        print(f"Processing conversation...")
        if file_path:
            print(f"Source: {file_path}")
        
        # Process the conversation
        output = tts_tool.process_conversation(conversation_data)
        
        # Save output
        tts_tool.save_output(output)
        
        print(f"✓ Generated {len(output['lines'])} audio files")
        print(f"✓ Total duration: {output['total_duration']:.2f} seconds")
        print(f"✓ Output directory: {output['output_directory']}")
        
        return output
    
    except Exception as e:
        print(f"✗ Error processing conversation: {e}")
        if file_path:
            print(f"  Source file: {file_path}")
        return None


def process_files(input_path: str, output_dir: str = "output", 
                 tts_provider: str = "google", **tts_kwargs) -> List[Dict]:
    """Process all JSON files in the input path."""
    
    # Find all JSON files
    try:
        json_files = find_json_files(input_path)
        print(f"Found {len(json_files)} JSON file(s) to process")
    except ValueError as e:
        print(f"Error: {e}")
        return []
    
    # Initialize TTS tool
    tts_tool = DialogueTTS(output_dir=output_dir, tts_provider=tts_provider, **tts_kwargs)
    
    # Show provider information
    provider_info = tts_tool.get_tts_provider_info()
    print(f"Using TTS provider: {provider_info['provider_name']}")
    
    results = []
    successful = 0
    failed = 0
    
    # Process each file
    for i, file_path in enumerate(json_files, 1):
        print(f"\n[{i}/{len(json_files)}] Processing: {os.path.basename(file_path)}")
        
        try:
            # Load conversation data
            conversation_data = load_conversation_from_file(file_path)
            
            # Validate conversation
            if not validate_conversation(conversation_data, file_path):
                failed += 1
                continue
            
            # Process conversation
            output = process_single_conversation(tts_tool, conversation_data, file_path)
            
            if output:
                results.append(output)
                successful += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"✗ Error processing {file_path}: {e}")
            failed += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    print(f"📁 Output directory: {output_dir}")
    
    return results


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Process dialogue conversations and generate voice files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single JSON file
  python main.py conversation.json
  
  # Process all JSON files in a directory
  python main.py conversations/
  
  # Specify output directory and TTS provider
  python main.py conversation.json --output my_output --provider google --lang en
  
  # Process with custom TTS settings
  python main.py conversations/ --provider google --lang es --tld com
        """
    )
    
    parser.add_argument(
        'input',
        help='Input JSON file or directory containing JSON files'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--provider', '-p',
        default='google',
        choices=['google'],  # Add more providers as they become available
        help='TTS provider to use (default: google)'
    )
    
    parser.add_argument(
        '--lang',
        default='en',
        help='Language for TTS (default: en)'
    )
    
    parser.add_argument(
        '--tld',
        default='com',
        help='Top-level domain for Google TTS (default: com)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input path
    if not os.path.exists(args.input):
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)
    
    # Prepare TTS kwargs
    tts_kwargs = {
        'lang': args.lang,
        'tld': args.tld
    }
    
    # Process files
    try:
        results = process_files(
            input_path=args.input,
            output_dir=args.output,
            tts_provider=args.provider,
            **tts_kwargs
        )
        
        if not results:
            print("No conversations were successfully processed.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
