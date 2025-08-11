#!/usr/bin/env python3
"""
File utility functions
Handles file operations, output management, and JSON handling.
"""

import json
import os
from typing import Dict, Optional
from datetime import datetime
import uuid


def save_json_output(output_data: Dict, output_path: str) -> bool:
    """
    Save output data to JSON file.
    
    Args:
        output_data: Dictionary to save
        output_path: Path where to save the JSON file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"Output saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving output to {output_path}: {e}")
        return False


def generate_unique_id() -> str:
    """
    Generate a unique identifier for dialogues.
    
    Returns:
        Unique string identifier
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_part = uuid.uuid4().hex[:8]
    return f"dialog_{timestamp}_{unique_part}"


def create_dialogue_directory_structure(base_output_dir: str, dialog_id: str) -> tuple[str, str]:
    """
    Create directory structure for a dialogue.
    
    Args:
        base_output_dir: Base output directory
        dialog_id: Dialog identifier
    
    Returns:
        Tuple of (dialogue_dir, audio_dir)
    """
    dialogue_dir = os.path.join(base_output_dir, dialog_id)
    audio_dir = os.path.join(dialogue_dir, "audio")
    
    os.makedirs(dialogue_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    
    return dialogue_dir, audio_dir


def get_output_paths(dialogue_dir: str, dialog_id: str) -> Dict[str, str]:
    """
    Get all output file paths for a dialogue.
    
    Args:
        dialogue_dir: Directory for the dialogue
        dialog_id: Dialog identifier
    
    Returns:
        Dictionary with path keys and values
    """
    return {
        "json_output": os.path.join(dialogue_dir, "output.json"),
        "merged_audio": os.path.join(dialogue_dir, "output.mp3"),
        "audio_dir": os.path.join(dialogue_dir, "audio")
    }


def format_output_data(dialog_id: str, speakers: list, lines: list, 
                      total_duration: float, output_directory: str,
                      merged_audio_file: Optional[str] = None) -> Dict:
    """
    Format the final output data structure.
    
    Args:
        dialog_id: Dialog identifier
        speakers: List of speakers
        lines: List of dialogue lines
        total_duration: Total duration in seconds
        output_directory: Output directory path
        merged_audio_file: Optional merged audio filename
    
    Returns:
        Formatted output dictionary
    """
    output = {
        "dialog_id": dialog_id,
        "speakers": speakers,
        "total_duration": total_duration,
        "lines": lines,
        "output_directory": output_directory
    }
    
    if merged_audio_file:
        output["merged_audio_file"] = merged_audio_file
    
    return output


def validate_file_path(file_path: str) -> bool:
    """
    Validate if a file path exists and is accessible.
    
    Args:
        file_path: Path to validate
    
    Returns:
        True if valid, False otherwise
    """
    return os.path.exists(file_path) and os.access(file_path, os.R_OK)


def ensure_output_directory(output_dir: str) -> None:
    """
    Ensure the output directory exists.
    
    Args:
        output_dir: Output directory path
    """
    os.makedirs(output_dir, exist_ok=True)
