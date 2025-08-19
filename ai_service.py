import openai
import os
import tempfile
import requests
from elevenlabs import generate, save, set_api_key, Voice, VoiceSettings
from elevenlabs.api import History
from typing import List, Dict, Optional
from database import AIKnowledgeDatabase

class AIService:
    def __init__(self, api_key: str, model: str = "gpt-4", max_tokens: int = 1000, temperature: float = 0.7):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.db = AIKnowledgeDatabase()
        
        # Set up ElevenLabs API key
        elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        if elevenlabs_api_key:
            set_api_key(elevenlabs_api_key)
    
    def speech_to_text(self, audio_file_path: str) -> str:
        """Convert speech from audio file to text using OpenAI's Whisper API."""
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
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
    
    def speech_to_speech(self, audio_file_path: str, output_path: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> str:
        """Complete speech-to-speech pipeline using ElevenLabs."""
        try:
            # Step 1: Convert speech to text
            text = self.speech_to_text(audio_file_path)
            
            if not text:
                return ""
            
            # Step 2: Generate AI response
            ai_response = self.generate_response(text)
            
            # Step 3: Convert AI response to speech
            if self.text_to_speech(ai_response, output_path, voice_id):
                return ai_response
            else:
                return ""
                
        except Exception as e:
            print(f"Error in speech to speech: {e}")
            return ""
    
    def get_available_voices(self) -> List[Dict]:
        """Get list of available ElevenLabs voices."""
        try:
            from elevenlabs import voices
            available_voices = voices()
            return [
                {
                    'voice_id': voice.voice_id,
                    'name': voice.name,
                    'category': voice.category
                }
                for voice in available_voices
            ]
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    def convert_ogg_to_wav(self, ogg_path: str, wav_path: str) -> bool:
        """Convert OGG audio file to WAV format."""
        try:
            audio = AudioSegment.from_ogg(ogg_path)
            audio.export(wav_path, format="wav")
            return True
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
        """Generate a response using ChatGPT with relevant knowledge context."""
        # Get relevant knowledge from database
        relevant_knowledge = self.get_relevant_knowledge(user_message)
        
        # Build the system prompt
        system_prompt = """You are an AI assistant with expertise in artificial intelligence. You have access to a knowledge database about AI topics. 

When answering questions:
1. Use the provided knowledge base information when relevant
2. Provide accurate, helpful, and informative responses
3. If the knowledge base doesn't contain relevant information, use your general AI knowledge
4. Keep responses concise but comprehensive
5. Be conversational and friendly

Always cite sources when possible and acknowledge when information comes from the knowledge base."""

        # Build the user message with context
        if relevant_knowledge:
            user_prompt = f"Context from knowledge base:\n{relevant_knowledge}\n\nUser question: {user_message}"
        else:
            user_prompt = f"User question: {user_message}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            ai_response = response.choices[0].message.content
            
            # Save conversation to database if user_id is provided
            if user_id:
                self.db.save_conversation(user_id, user_message, ai_response)
            
            return ai_response
            
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    
    def add_knowledge_to_database(self, title: str, content: str, category: str = None, tags: List[str] = None):
        """Add new knowledge to the database."""
        self.db.add_knowledge(title, content, category, tags)
    
    def get_conversation_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get conversation history for a user."""
        return self.db.get_user_conversation_history(user_id, limit)
    
    def search_knowledge_database(self, query: str, limit: int = 5) -> List[Dict]:
        """Search the knowledge database."""
        return self.db.search_knowledge(query, limit)
