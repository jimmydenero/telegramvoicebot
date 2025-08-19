#!/usr/bin/env python3
"""
Test script for ElevenLabs voice functionality
"""

import os
import tempfile
from dotenv import load_dotenv
from elevenlabs import generate, save, set_api_key, voices

# Load environment variables
load_dotenv()

def test_elevenlabs_setup():
    """Test ElevenLabs API setup and voice listing."""
    print("🎤 Testing ElevenLabs Setup...")
    
    # Set API key
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ ELEVENLABS_API_KEY not found in environment variables")
        return False
    
    try:
        set_api_key(api_key)
        print("✅ ElevenLabs API key set successfully")
        
        # Get available voices
        available_voices = voices()
        print(f"✅ Found {len(available_voices)} available voices")
        
        # Show first few voices
        print("\n📋 Sample Voices:")
        for i, voice in enumerate(available_voices[:5], 1):
            print(f"  {i}. {voice.name} (ID: {voice.voice_id})")
        
        return True
        
    except Exception as e:
        print(f"❌ ElevenLabs setup failed: {e}")
        return False

def test_text_to_speech():
    """Test ElevenLabs text-to-speech functionality."""
    print("\n🎵 Testing Text-to-Speech...")
    
    test_text = "Hello! This is a test of the ElevenLabs text to speech functionality. The voice should sound very natural and human-like."
    
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_mp3:
        mp3_path = temp_mp3.name
        
        try:
            print(f"📝 Converting text to speech: '{test_text[:50]}...'")
            
            # Generate audio using ElevenLabs
            audio = generate(
                text=test_text,
                voice="21m00Tcm4TlvDq8ikWAM",  # Rachel voice
                model="eleven_monolingual_v1"
            )
            
            # Save the audio
            save(audio, mp3_path)
            
            print(f"✅ Text-to-speech successful! Audio saved to: {mp3_path}")
            print(f"📁 File size: {os.path.getsize(mp3_path)} bytes")
            
        except Exception as e:
            print(f"❌ Text-to-speech failed: {e}")
        finally:
            # Clean up
            if os.path.exists(mp3_path):
                os.unlink(mp3_path)
    
    print("✅ Text-to-speech test completed!")

def test_different_voices():
    """Test different ElevenLabs voices."""
    print("\n🎭 Testing Different Voices...")
    
    test_text = "This is a test of different voices."
    
    # Test with a few different voice IDs
    voice_ids = [
        "21m00Tcm4TlvDq8ikWAM",  # Rachel
        "AZnzlk1XvdvUeBnXmlld",  # Domi
        "EXAVITQu4vr4xnSDxMaL"   # Bella
    ]
    
    for i, voice_id in enumerate(voice_ids, 1):
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_mp3:
            mp3_path = temp_mp3.name
            
            try:
                print(f"🎤 Testing voice {i} (ID: {voice_id})")
                
                audio = generate(
                    text=test_text,
                    voice=voice_id,
                    model="eleven_monolingual_v1"
                )
                
                save(audio, mp3_path)
                print(f"✅ Voice {i} successful! Size: {os.path.getsize(mp3_path)} bytes")
                
            except Exception as e:
                print(f"❌ Voice {i} failed: {e}")
            finally:
                if os.path.exists(mp3_path):
                    os.unlink(mp3_path)
    
    print("✅ Different voices test completed!")

if __name__ == "__main__":
    print("🎤 ElevenLabs Voice Functionality Tests")
    print("=" * 50)
    
    if test_elevenlabs_setup():
        test_text_to_speech()
        test_different_voices()
        
        print("\n🎉 All ElevenLabs tests completed!")
        print("\nTo use the voice functionality with the bot:")
        print("1. Set up your .env file with ELEVENLABS_API_KEY")
        print("2. Run: python3 telegram_bot.py")
        print("3. Send voice messages to your bot!")
    else:
        print("\n❌ ElevenLabs setup failed. Please check your API key.")
