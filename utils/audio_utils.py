#!/usr/bin/env python3
"""
Audio processing utilities
Handles audio file operations, merging, and duration calculations.
"""

import os
from typing import List, Tuple, Optional
from pydub import AudioSegment


def get_audio_duration(audio_path: str) -> float:
    """
    Get duration of audio file in seconds using pydub.
    
    Args:
        audio_path: Path to the audio file
    
    Returns:
        Duration in seconds
    """
    try:
        audio = AudioSegment.from_mp3(audio_path)
        return len(audio) / 1000.0  # Convert milliseconds to seconds
    except Exception as e:
        print(f"Error getting duration for {audio_path}: {e}")
        return 2.0  # Default fallback


def save_audio_file(temp_mp3_path: str, output_filename: str, target_dir: str) -> Optional[str]:
    """
    Save MP3 file with final filename.
    
    Args:
        temp_mp3_path: Path to temporary MP3 file
        output_filename: Desired output filename
        target_dir: Directory to save the file in
    
    Returns:
        Path to the saved file, or None if failed
    """
    try:
        final_path = os.path.join(target_dir, output_filename)
        # Rename the temporary file to final filename
        os.rename(temp_mp3_path, final_path)
        return final_path
    except Exception as e:
        print(f"Error saving audio file {output_filename}: {e}")
        return None


def merge_audio_files(audio_dir: str, dialog_id: str, output_dir: str) -> Optional[str]:
    """
    Merge all individual MP3 files into a single output.mp3 file.
    
    Args:
        audio_dir: Directory containing individual audio files
        dialog_id: Dialog ID to match files
        output_dir: Directory to save merged file
    
    Returns:
        Path to merged audio file, or None if failed
    """
    try:
        output_path = os.path.join(output_dir, "output.mp3")
        
        # Get all MP3 files in the audio directory, sorted by index
        mp3_files = []
        for filename in os.listdir(audio_dir):
            if filename.endswith('.mp3') and filename.startswith(f"{dialog_id}_"):
                # Extract index from filename (e.g., "dialog_id_0.mp3" -> 0)
                try:
                    index = int(filename.split('_')[-1].replace('.mp3', ''))
                    mp3_files.append((index, os.path.join(audio_dir, filename)))
                except ValueError:
                    continue
        
        # Sort by index to maintain conversation order
        mp3_files.sort(key=lambda x: x[0])
        
        if not mp3_files:
            print("No MP3 files found to merge")
            return None
        
        # Merge audio files
        print(f"Merging {len(mp3_files)} audio files...")
        combined = AudioSegment.empty()
        
        for index, file_path in mp3_files:
            try:
                audio = AudioSegment.from_mp3(file_path)
                combined += audio
                print(f"  Added file {index}: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"  Error loading {file_path}: {e}")
                continue
        
        # Export merged audio
        combined.export(output_path, format="mp3")
        print(f"✓ Merged audio saved to: {output_path}")
        print(f"✓ Total duration: {len(combined) / 1000.0:.2f} seconds")
        
        return output_path
        
    except Exception as e:
        print(f"Error merging audio files: {e}")
        return None


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        directory_path: Path to the directory
    """
    os.makedirs(directory_path, exist_ok=True)


def get_audio_files_in_order(audio_dir: str, dialog_id: str) -> List[Tuple[int, str]]:
    """
    Get all audio files for a dialog in order by index.
    
    Args:
        audio_dir: Directory containing audio files
        dialog_id: Dialog ID to match files
    
    Returns:
        List of (index, file_path) tuples sorted by index
    """
    mp3_files = []
    for filename in os.listdir(audio_dir):
        if filename.endswith('.mp3') and filename.startswith(f"{dialog_id}_"):
            try:
                index = int(filename.split('_')[-1].replace('.mp3', ''))
                mp3_files.append((index, os.path.join(audio_dir, filename)))
            except ValueError:
                continue
    
    return sorted(mp3_files, key=lambda x: x[0])
