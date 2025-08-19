import os
import tempfile
import requests
import json
from elevenlabs import generate, save, set_api_key, voices, clone
from elevenlabs.api import History
from typing import List, Dict, Optional
from .database import AIKnowledgeDatabase

class AIService:
    def __init__(self, elevenlabs_api_key: str = None):
        self.db = AIKnowledgeDatabase()
        
        # Set up ElevenLabs API key
        api_key = elevenlabs_api_key or os.getenv('ELEVENLABS_API_KEY')
        if api_key:
            set_api_key(api_key)
            self.api_key = api_key
        else:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
    
    def speech_to_text(self, audio_file_path: str) -> str:
        """Convert speech from audio file to text using ElevenLabs Speech-to-Text API."""
        try:
            print(f"Starting speech to text for file: {audio_file_path}")
            url = "https://api.elevenlabs.io/v1/speech-to-text"
            
            with open(audio_file_path, "rb") as audio_file:
                files = {"file": audio_file}
                headers = {"xi-api-key": self.api_key}
                
                print("Sending request to ElevenLabs Speech-to-Text API")
                response = requests.post(url, files=files, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    text = result.get("text", "")
                    print(f"Speech-to-text successful: '{text}'")
                    return text
                else:
                    print(f"Speech-to-text error: {response.status_code} - {response.text}")
                    return ""
                    
        except Exception as e:
            print(f"Error in speech to text: {e}")
            return ""
    
    def text_to_speech(self, text: str, output_path: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bool:
        """Convert text to speech using ElevenLabs and save as audio file."""
        try:
            # Generate audio using ElevenLabs
            audio = generate(
                text=text,
                voice=voice_id,
                model="eleven_monolingual_v1"
            )
            
            # Save the audio
            save(audio, output_path)
            return True
        except Exception as e:
            print(f"Error in text to speech: {e}")
            return False
    
    def voice_to_voice(self, input_audio_path: str, output_path: str, target_voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> str:
        """Direct voice-to-voice conversion using ElevenLabs Voice Conversion API."""
        try:
            print(f"Starting voice-to-voice conversion for file: {input_audio_path}")
            
            # Check if file exists and get file size
            if not os.path.exists(input_audio_path):
                print(f"Error: Input file does not exist: {input_audio_path}")
                return ""
            
            file_size = os.path.getsize(input_audio_path)
            print(f"Input file size: {file_size} bytes")
            
            url = "https://api.elevenlabs.io/v1/voice-conversion"
            
            with open(input_audio_path, "rb") as audio_file:
                files = {"input_file": audio_file}
                data = {"voice_id": target_voice_id}
                headers = {"xi-api-key": self.api_key}
                
                print(f"Sending request to ElevenLabs Voice Conversion API with voice_id: {target_voice_id}")
                print(f"API Key (first 10 chars): {self.api_key[:10]}...")
                
                response = requests.post(url, files=files, data=data, headers=headers)
                
                print(f"Response status code: {response.status_code}")
                print(f"Response headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    # Save the converted audio
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    print(f"Voice-to-voice conversion successful. Output file size: {os.path.getsize(output_path)} bytes")
                    return "Voice converted successfully"
                else:
                    print(f"Voice-to-voice error: {response.status_code} - {response.text}")
                    return ""
                    
        except Exception as e:
            print(f"Error in voice to voice conversion: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def fallback_voice_conversion(self, input_audio_path: str, output_path: str, target_voice_id: str) -> str:
        """Fallback: Convert speech to text then back to speech with target voice."""
        try:
            print(f"Starting fallback voice conversion for file: {input_audio_path}")
            
            # Step 1: Convert speech to text
            text = self.speech_to_text(input_audio_path)
            print(f"Speech to text result: '{text}'")
            
            if not text:
                print("No text extracted from speech")
                return ""
            
            # Step 2: Convert text to speech with target voice
            print(f"Converting text to speech with voice ID: {target_voice_id}")
            if self.text_to_speech(text, output_path, target_voice_id):
                print("Text to speech successful")
                return "Voice converted successfully (fallback method)"
            else:
                print("Text to speech failed")
                return ""
                
        except Exception as e:
            print(f"Error in fallback voice conversion: {e}")
            return ""
    
    def speech_to_speech(self, audio_file_path: str, output_path: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> str:
        """Complete speech-to-speech pipeline using ElevenLabs."""
        try:
            # Step 1: Convert speech to text
            text = self.speech_to_text(audio_file_path)
            
            if not text:
                return ""
            
            # Step 2: Generate a simple response (no OpenAI needed)
            ai_response = self.generate_simple_response(text)
            
            # Step 3: Convert AI response to speech
            if self.text_to_speech(ai_response, output_path, voice_id):
                return ai_response
            else:
                return ""
                
        except Exception as e:
            print(f"Error in speech to speech: {e}")
            return ""
    
    def generate_simple_response(self, user_message: str) -> str:
        """Generate a simple response without using OpenAI."""
        # Simple response logic - you can enhance this
        message_lower = user_message.lower()
        
        if "hello" in message_lower or "hi" in message_lower:
            return "Hello! I'm your AI assistant. How can I help you today?"
        elif "how are you" in message_lower:
            return "I'm doing great! Thanks for asking. How can I assist you?"
        elif "what can you do" in message_lower:
            return "I can help you with various tasks, answer questions, and convert voice messages. Just let me know what you need!"
        elif "thank you" in message_lower or "thanks" in message_lower:
            return "You're welcome! I'm happy to help."
        elif "bye" in message_lower or "goodbye" in message_lower:
            return "Goodbye! Have a great day!"
        else:
            return f"I received your message: '{user_message}'. This is a simple response. You can enhance this with more sophisticated logic."
    
    def get_available_voices(self) -> List[Dict]:
        """Get list of available ElevenLabs voices - only custom voices."""
        try:
            available_voices = voices()
            # Filter to only show custom voices (not default ones)
            custom_voices = [
                {
                    'voice_id': voice.voice_id,
                    'name': voice.name,
                    'category': voice.category
                }
                for voice in available_voices
                if voice.category == "cloned" or voice.category == "generated" or voice.category == "custom"
            ]
            return custom_voices
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    def convert_ogg_to_wav(self, ogg_path: str, wav_path: str) -> bool:
        """Convert OGG audio file to WAV format."""
        try:
            # Simple conversion using ffmpeg or similar
            import subprocess
            result = subprocess.run([
                'ffmpeg', '-i', ogg_path, '-acodec', 'pcm_s16le', 
                '-ar', '44100', '-ac', '2', wav_path
            ], capture_output=True, text=True)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error converting audio format: {e}")
            return False
    
    def get_relevant_knowledge(self, query: str) -> str:
        """Retrieve relevant knowledge from the database based on the query."""
        knowledge_items = self.db.search_knowledge(query, limit=3)
        
        if not knowledge_items:
            return ""
        
        knowledge_text = "Relevant AI knowledge:\n\n"
        for item in knowledge_items:
            knowledge_text += f"Title: {item['title']}\n"
            knowledge_text += f"Category: {item['category']}\n"
            knowledge_text += f"Content: {item['content']}\n"
            knowledge_text += f"Tags: {', '.join(item['tags']) if item['tags'] else 'None'}\n"
            knowledge_text += "-" * 50 + "\n"
        
        return knowledge_text
    
    def generate_response(self, user_message: str, user_id: int = None) -> str:
        """Generate a response using the simple response generator."""
        # Get relevant knowledge from database
        relevant_knowledge = self.get_relevant_knowledge(user_message)
        
        # Generate response
        ai_response = self.generate_simple_response(user_message)
        
        # Save conversation to database if user_id is provided
        if user_id:
            self.db.save_conversation(user_id, user_message, ai_response)
        
        return ai_response
    
    def add_knowledge_to_database(self, title: str, content: str, category: str = None, tags: List[str] = None):
        """Add new knowledge to the database."""
        self.db.add_knowledge(title, content, category, tags)
    
    def get_conversation_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get conversation history for a user."""
        return self.db.get_user_conversation_history(user_id, limit)
    
    def search_knowledge_database(self, query: str, limit: int = 5) -> List[Dict]:
        """Search the knowledge database."""
        return self.db.search_knowledge(query, limit)
