#!/usr/bin/env python3
"""
Conversation parsing utilities
Handles parsing and validation of conversation content.
"""

import re
from typing import Dict, List


def parse_conversation_content(content: str) -> List[Dict]:
    """
    Parse conversation content into individual dialogue lines.
    
    Args:
        content: String containing conversation in format "Speaker: Text, Speaker: Text"
    
    Returns:
        List of dictionaries with speaker, text, and index information
    """
    lines = []
    # Split by speaker patterns like "Jane:", "David:"
    pattern = r'([A-Za-z]+):\s*([^:]+?)(?=\s*[A-Za-z]+:|$)'
    matches = re.findall(pattern, content)
    
    for i, (speaker, text) in enumerate(matches):
        lines.append({
            "index": i,
            "speaker": speaker.strip(),
            "text": text.strip(),
            "start_time": 0,  # Will be calculated
            "duration": 0,     # Will be calculated
            "audio_file": f"dialog_{i}.mp3"
        })
    
    return lines


def validate_conversation_data(data: Dict) -> tuple[bool, str]:
    """
    Validate conversation data structure.
    
    Args:
        data: Dictionary containing conversation data
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check required fields
        if not isinstance(data.get('speakers'), list):
            return False, "'speakers' must be a list"
        
        if not isinstance(data.get('content'), str):
            return False, "'content' must be a string"
        
        # Validate speakers
        for i, speaker in enumerate(data['speakers']):
            if not isinstance(speaker, dict):
                return False, f"Speaker {i} must be a dictionary"
            
            if 'name' not in speaker or 'gender' not in speaker:
                return False, f"Speaker {i} must have 'name' and 'gender' fields"
            
            if speaker['gender'] not in ['male', 'female']:
                return False, f"Speaker {i} gender must be 'male' or 'female', got: {speaker['gender']}"
        
        # Check if content has any dialogue
        if not data['content'].strip():
            return False, "'content' cannot be empty"
        
        # Validate dialog_id if provided
        if 'dialog_id' in data:
            if not isinstance(data['dialog_id'], str):
                return False, "'dialog_id' must be a string"
            if not data['dialog_id'].strip():
                return False, "'dialog_id' cannot be empty"
        
        return True, ""
        
    except Exception as e:
        return False, f"Validation error: {e}"


def extract_speaker_mapping(speakers: List[Dict]) -> Dict[str, Dict]:
    """
    Create a mapping of speaker names to their information.
    
    Args:
        speakers: List of speaker dictionaries
    
    Returns:
        Dictionary mapping speaker names to speaker info
    """
    return {s["name"]: s for s in speakers}


def get_dialog_id(data: Dict) -> str:
    """
    Extract or generate dialog ID from conversation data.
    
    Args:
        data: Conversation data dictionary
    
    Returns:
        Dialog ID string
    """
    return data.get("dialog_id", "").strip()
