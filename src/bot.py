import os
import logging
import tempfile
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from dotenv import load_dotenv
from .ai_service import AIService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramAIBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.ai_service = AIService(
            elevenlabs_api_key=os.getenv('ELEVENLABS_API_KEY')
        )
        
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
        
        # User states for voice selection
        self.user_states = {}
        
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all bot command and message handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("voices", self.voices_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(MessageHandler(filters.VOICE, self.handle_voice_message))
        self.application.add_handler(MessageHandler(filters.AUDIO, self.handle_audio_message))
        
        # Callback query handler for inline buttons
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """
Click to Generate
        """
        
        keyboard = [
            [InlineKeyboardButton("Generate Voice", callback_data="generate_voice")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = """
ElevenLabs Voice Bot Help

Commands:
/start - Welcome message and main menu
/help - Show this help information
/voices - List available ElevenLabs voices

How to Use:
1. Click "Generate Voice" button
2. Select a voice from the list
3. Send text or voice message
4. Get converted audio back

Features:
Text-to-Speech with custom voices
Voice-to-Voice conversion
Custom voice selection
Interactive voice buttons

Just click "Generate Voice" to start!
        """
        await update.message.reply_text(help_text)
    
    async def voices_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /voices command - list available ElevenLabs voices."""
        voices = self.ai_service.get_available_voices()
        
        if not voices:
            await update.message.reply_text(
                "❌ Could not retrieve available voices. Make sure your ELEVENLABS_API_KEY is set correctly."
            )
            return
        
        response = "Available ElevenLabs Voices:\n\n"
        for i, voice in enumerate(voices[:10], 1):  # Show first 10 voices
            response += f"{i}. {voice['name']}\n"
            response += f"   ID: {voice['voice_id']}\n"
            response += f"   Category: {voice['category']}\n\n"
        
        if len(voices) > 10:
            response += f"... and {len(voices) - 10} more voices available.\n\n"
        
        response += "Tip: Use the Generate Voice button to select and use these voices."
        
        await update.message.reply_text(response)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages for text-to-speech."""
        user_id = update.effective_user.id
        
        # Check if user is in voice selection state
        if user_id in self.user_states and self.user_states[user_id].get('waiting_for_text'):
            voice_id = self.user_states[user_id].get('selected_voice')
            if voice_id:
                # Generate speech from text
                await self.generate_speech_from_text(update, context, update.message.text, voice_id)
                # Clear user state
                del self.user_states[user_id]
            else:
                await update.message.reply_text("Please select a voice first using the Generate Voice button.")
        else:
            # Show the generate voice button
            keyboard = [
                [InlineKeyboardButton("Generate Voice", callback_data="generate_voice")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Send me some text and I'll convert it to speech! Click the button below to select a voice:",
                reply_markup=reply_markup
            )
    
    async def handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages for voice-to-voice conversion."""
        user_id = update.effective_user.id
        
        # Check if user has selected a voice
        if user_id in self.user_states and self.user_states[user_id].get('selected_voice'):
            voice_id = self.user_states[user_id].get('selected_voice')
            await self.convert_voice_to_voice(update, context, voice_id)
        else:
            # Show voice selection first
            keyboard = [
                [InlineKeyboardButton("Generate Voice", callback_data="generate_voice")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "I can convert your voice to a different voice! Click the button below to select a target voice:",
                reply_markup=reply_markup
            )
    
    async def handle_audio_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle audio messages for voice-to-voice conversion."""
        user_id = update.effective_user.id
        
        # Check if user has selected a voice
        if user_id in self.user_states and self.user_states[user_id].get('selected_voice'):
            voice_id = self.user_states[user_id].get('selected_voice')
            await self.convert_voice_to_voice(update, context, voice_id, is_audio=True)
        else:
            # Show voice selection first
            keyboard = [
                [InlineKeyboardButton("Generate Voice", callback_data="generate_voice")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "I can convert your audio to a different voice! Click the button below to select a target voice:",
                reply_markup=reply_markup
            )
    
    async def generate_speech_from_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, voice_id: str):
        """Generate speech from text using selected voice."""
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_mp3:
                mp3_path = temp_mp3.name
                
                if self.ai_service.text_to_speech(text, mp3_path, voice_id):
                    with open(mp3_path, 'rb') as audio_file:
                        await context.bot.send_audio(
                            chat_id=update.effective_chat.id,
                            audio=audio_file,
                            title="Generated Voice",
                            performer="ElevenLabs"
                        )
                    
                    # Show Generate Voice button after success
                    keyboard = [[InlineKeyboardButton("Generate Voice", callback_data="generate_voice")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await update.message.reply_text("Click to Generate", reply_markup=reply_markup)
                else:
                    await update.message.reply_text("Sorry, I couldn't generate the voice. Please try again.")
                    
                    # Show Generate Voice button after failure
                    keyboard = [[InlineKeyboardButton("Generate Voice", callback_data="generate_voice")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await update.message.reply_text("Click to Generate", reply_markup=reply_markup)
            
            # Clean up
            if os.path.exists(mp3_path):
                os.unlink(mp3_path)
                
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            await update.message.reply_text("Sorry, I encountered an error while generating the voice.")
            
            # Show Generate Voice button after error
            keyboard = [[InlineKeyboardButton("Generate Voice", callback_data="generate_voice")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Click to Generate", reply_markup=reply_markup)
    
    async def convert_voice_to_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE, voice_id: str, is_audio: bool = False):
        """Convert voice to voice using selected voice."""
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Get the voice/audio file
            if is_audio:
                file_obj = update.message.audio
                file = await context.bot.get_file(file_obj.file_id)
            else:
                file_obj = update.message.voice
                file = await context.bot.get_file(file_obj.file_id)
            
            # Download the file
            with tempfile.NamedTemporaryFile(suffix='.ogg' if not is_audio else '.mp3', delete=False) as temp_input:
                input_path = temp_input.name
                await file.download_to_drive(input_path)
            
            # Convert OGG to WAV if needed
            if not is_audio:
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                    wav_path = temp_wav.name
                    if not self.ai_service.convert_ogg_to_wav(input_path, wav_path):
                        await update.message.reply_text("Sorry, I couldn't process the audio file.")
                        return
                    input_path = wav_path
            
            # Convert voice to voice
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_mp3:
                mp3_path = temp_mp3.name
                
                result = self.ai_service.voice_to_voice(input_path, mp3_path, voice_id)
                
                if result:
                    with open(mp3_path, 'rb') as audio_file:
                        await context.bot.send_audio(
                            chat_id=update.effective_chat.id,
                            audio=audio_file,
                            title="Voice Converted",
                            performer="ElevenLabs Voice Conversion"
                        )
                    
                    # Show Generate Voice button after success
                    keyboard = [[InlineKeyboardButton("Generate Voice", callback_data="generate_voice")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await update.message.reply_text("Click to Generate", reply_markup=reply_markup)
                else:
                    await update.message.reply_text("Sorry, I couldn't convert your voice. Please try again.")
                    
                    # Show Generate Voice button after failure
                    keyboard = [[InlineKeyboardButton("Generate Voice", callback_data="generate_voice")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await update.message.reply_text("Click to Generate", reply_markup=reply_markup)
            
            # Clean up
            os.unlink(input_path)
            if os.path.exists(mp3_path):
                os.unlink(mp3_path)
                
        except Exception as e:
            logger.error(f"Error converting voice: {e}")
            await update.message.reply_text("Sorry, I encountered an error while converting your voice.")
            
            # Show Generate Voice button after error
            keyboard = [[InlineKeyboardButton("Generate Voice", callback_data="generate_voice")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Click to Generate", reply_markup=reply_markup)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries from inline buttons."""
        query = update.callback_query
        await query.answer()
        
        if query.data == "generate_voice":
            # Show voice selection
            voices = self.ai_service.get_available_voices()
            
            if not voices:
                await query.edit_message_text(
                    "Could not retrieve voices. Please check your ElevenLabs API key."
                )
                return
            
            # Create voice selection buttons
            keyboard = []
            for voice in voices[:8]:  # Show first 8 voices
                keyboard.append([
                    InlineKeyboardButton(
                        f"{voice['name']}", 
                        callback_data=f"select_voice_{voice['voice_id']}"
                    )
                ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "Select a voice",
                reply_markup=reply_markup
            )
        
        elif query.data.startswith("select_voice_"):
            voice_id = query.data.replace("select_voice_", "")
            user_id = update.effective_user.id
            
            # Store selected voice in user state
            self.user_states[user_id] = {
                'selected_voice': voice_id,
                'waiting_for_text': True
            }
            
            await query.edit_message_text(
                "Voice Selected! Now send me some text to convert to speech, or send a voice message to convert it to the selected voice."
            )
    
    def run(self):
        """Start the bot."""
        logger.info("Starting ElevenLabs Voice Bot...")
        self.application.run_polling()

if __name__ == "__main__":
    bot = TelegramAIBot()
    bot.run()
