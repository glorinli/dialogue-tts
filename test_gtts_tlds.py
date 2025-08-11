#!/usr/bin/env python3
"""
Test script for Google TTS TLDs
Tests different top-level domains to see which ones are actually supported and working.
"""

import os
import sys
from gtts import gTTS
import time

def test_tld(tld, text="Hello, this is a test of the TTS system.", output_dir="test_output"):
    """Test a specific TLD with Google TTS."""
    try:
        print(f"Testing TLD: {tld}")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create TTS object
        tts = gTTS(text=text, lang='en', tld=tld, slow=False)
        
        # Generate filename
        filename = f"test_{tld}.mp3"
        filepath = os.path.join(output_dir, filename)
        
        # Save audio
        print(f"  Generating speech...")
        start_time = time.time()
        tts.save(filepath)
        end_time = time.time()
        
        # Check if file was created and has content
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            print(f"  ✓ Success! File: {filename}")
            print(f"  ✓ File size: {os.path.getsize(filepath)} bytes")
            print(f"  ✓ Generation time: {end_time - start_time:.2f} seconds")
            return True
        else:
            print(f"  ✗ Failed: File not created or empty")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_all_tlds():
    """Test all common TLDs that might work with Google TTS."""
    
    # Common TLDs to test
    tlds_to_test = [
        "com",      # US (most common)
        "co.uk",    # UK
        "com.au",   # Australia
        "ca",       # Canada
        "ie",       # Ireland
        "in",       # India
        "co.za",    # South Africa
        "co.nz",    # New Zealand
        "com.sg",   # Singapore
        "com.my",   # Malaysia
        "co.jp",    # Japan
        "co.kr",    # Korea
        "com.br",   # Brazil
        "com.mx",   # Mexico
        "com.ar",   # Argentina
        "com.pe",   # Peru
        "com.cl",   # Chile
        "com.ve",   # Venezuela
        "com.co",   # Colombia
        "com.ec",   # Ecuador
    ]
    
    print("Testing Google TTS TLDs")
    print("=" * 50)
    
    working_tlds = []
    failed_tlds = []
    
    for tld in tlds_to_test:
        success = test_tld(tld)
        if success:
            working_tlds.append(tld)
        else:
            failed_tlds.append(tld)
        print()  # Empty line for readability
        
        # Small delay to avoid overwhelming the service
        time.sleep(1)
    
    # Summary
    print("=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Working TLDs ({len(working_tlds)}): {', '.join(working_tlds)}")
    print(f"Failed TLDs ({len(failed_tlds)}): {', '.join(failed_tlds)}")
    
    if working_tlds:
        print(f"\nRecommended TLDs for voice variety:")
        for i, tld in enumerate(working_tlds[:4], 1):  # Top 4 working TLDs
            print(f"  {i}. {tld}")
    
    return working_tlds, failed_tlds

def test_specific_tlds():
    """Test specific TLDs that we're using in our voice configuration."""
    
    print("Testing TLDs from our voice configuration")
    print("=" * 50)
    
    # TLDs we're currently using
    current_tlds = ["com", "ca", "ie"]
    
    working_tlds = []
    
    for tld in current_tlds:
        success = test_tld(tld, f"This is a test of the {tld} TLD voice.")
        if success:
            working_tlds.append(tld)
        print()
        time.sleep(1)
    
    print("=" * 50)
    print("VOICE CONFIGURATION TLD TEST RESULTS")
    print("=" * 50)
    
    if len(working_tlds) == len(current_tlds):
        print("✓ All TLDs in our voice configuration are working!")
    else:
        print("✗ Some TLDs are not working:")
        for tld in current_tlds:
            status = "✓" if tld in working_tlds else "✗"
            print(f"  {status} {tld}")
    
    return working_tlds

if __name__ == "__main__":
    print("Google TTS TLD Test Suite")
    print("This script will test different TLDs to see which ones work with Google TTS")
    print()
    
    # Test our current voice configuration TLDs first
    print("1. Testing our current voice configuration TLDs...")
    working_current = test_specific_tlds()
    
    print("\n" + "="*60 + "\n")
    
    # Ask if user wants to test all TLDs
    response = input("Do you want to test all common TLDs? This will take longer. (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n2. Testing all common TLDs...")
        working_all, failed_all = test_all_tlds()
        
        print(f"\nSummary: {len(working_all)} working TLDs out of {len(working_all) + len(failed_all)} tested")
    else:
        print("Skipping comprehensive TLD testing.")
    
    print("\nTest completed! Check the 'test_output' directory for generated audio files.")
