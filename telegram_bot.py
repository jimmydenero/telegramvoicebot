import os
import logging
import tempfile
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from dotenv import load_dotenv
from ai_service import AIService

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
            api_key=os.getenv('OPENAI_API_KEY'),
            model=os.getenv('OPENAI_MODEL', 'gpt-4'),
            max_tokens=int(os.getenv('MAX_TOKENS', 1000)),
            temperature=float(os.getenv('TEMPERATURE', 0.7))
        )
        
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
        
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all bot command and message handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("search", self.search_command))
        self.application.add_handler(CommandHandler("history", self.history_command))
        self.application.add_handler(CommandHandler("add_knowledge", self.add_knowledge_command))
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
🤖 Welcome to the AI Knowledge Bot!

I'm here to help you with questions about artificial intelligence. I have access to a comprehensive knowledge database and can provide detailed answers.

**Available Commands:**
/start - Show this welcome message
/help - Show help information
/search <query> - Search the knowledge database
/history - Show your conversation history
/add_knowledge - Add new knowledge to the database
/voices - List available ElevenLabs voices

**Voice Features:**
🎤 Send voice messages and get voice responses!
📱 Supports both text and voice interactions

**Just ask me anything about AI!** 🧠
        """
        
        keyboard = [
            [InlineKeyboardButton("🔍 Search Knowledge", callback_data="search_kb")],
            [InlineKeyboardButton("📚 View History", callback_data="history")],
            [InlineKeyboardButton("➕ Add Knowledge", callback_data="add_knowledge")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = """
📖 **Bot Help Guide**

**Commands:**
• `/start` - Welcome message and main menu
• `/help` - Show this help information
• `/search <query>` - Search the AI knowledge database
• `/history` - View your conversation history
• `/add_knowledge` - Add new knowledge to the database

**Examples:**
• `/search machine learning`
• `/search neural networks`
• `/search AI ethics`

**Features:**
• 🤖 Powered by ChatGPT
• 📚 Access to AI knowledge database
• 💬 Conversation history tracking
• 🔍 Smart knowledge search
• 📝 Add your own knowledge
• 🎤 **Voice-to-Voice Chat** - Send voice messages and get voice responses!

**Voice Features:**
• Send voice messages to ask questions
• Get both text and voice responses
• Supports both voice messages and audio files
• Uses OpenAI Whisper for accurate speech recognition
• Uses ElevenLabs for natural, high-quality voice responses
• `/voices` - List available ElevenLabs voices

Just send me a text message or voice message with your AI question!
        """
        await update.message.reply_text(help_text)
    
    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /search command."""
        if not context.args:
            await update.message.reply_text("Please provide a search query. Example: `/search machine learning`")
            return
        
        query = " ".join(context.args)
        await update.message.reply_text(f"🔍 Searching for: {query}")
        
        # Search the knowledge database
        results = self.ai_service.search_knowledge_database(query, limit=5)
        
        if not results:
            await update.message.reply_text("No relevant knowledge found in the database.")
            return
        
        response = f"📚 **Search Results for '{query}':**\n\n"
        for i, item in enumerate(results, 1):
            response += f"**{i}. {item['title']}**\n"
            response += f"Category: {item['category']}\n"
            response += f"Content: {item['content'][:200]}...\n"
            if item['tags']:
                response += f"Tags: {', '.join(item['tags'])}\n"
            response += "\n"
        
        await update.message.reply_text(response)
    
    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /history command."""
        user_id = update.effective_user.id
        history = self.ai_service.get_conversation_history(user_id, limit=5)
        
        if not history:
            await update.message.reply_text("No conversation history found.")
            return
        
        response = "📚 **Your Recent Conversations:**\n\n"
        for i, conv in enumerate(history, 1):
            response += f"**{i}. {conv['timestamp']}**\n"
            response += f"Q: {conv['message'][:100]}...\n"
            response += f"A: {conv['response'][:100]}...\n\n"
        
        await update.message.reply_text(response)
    
    async def add_knowledge_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /add_knowledge command."""
        await update.message.reply_text(
            "To add knowledge to the database, please use the format:\n"
            "Title: [Your Title]\n"
            "Category: [Category]\n"
            "Tags: [tag1, tag2, tag3]\n"
            "Content: [Your content here]\n\n"
            "Or use the inline button below:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("➕ Add Knowledge", callback_data="add_knowledge")
            ]])
        )
    
    async def voices_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /voices command - list available ElevenLabs voices."""
        voices = self.ai_service.get_available_voices()
        
        if not voices:
            await update.message.reply_text(
                "❌ Could not retrieve available voices. Make sure your ELEVENLABS_API_KEY is set correctly."
            )
            return
        
        response = "🎤 **Available ElevenLabs Voices:**\n\n"
        for i, voice in enumerate(voices[:10], 1):  # Show first 10 voices
            response += f"**{i}. {voice['name']}**\n"
            response += f"   ID: `{voice['voice_id']}`\n"
            response += f"   Category: {voice['category']}\n\n"
        
        if len(voices) > 10:
            response += f"... and {len(voices) - 10} more voices available.\n\n"
        
        response += "💡 **Tip:** The bot uses the default voice (Rachel). You can customize this in the code."
        
        await update.message.reply_text(response)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle general text messages."""
        user_message = update.message.text
        user_id = update.effective_user.id
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Generate AI response
        try:
            ai_response = self.ai_service.generate_response(user_message, user_id)
            await update.message.reply_text(ai_response)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            await update.message.reply_text("Sorry, I encountered an error while processing your request. Please try again.")
    
    async def handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages using ElevenLabs speech-to-speech."""
        user_id = update.effective_user.id
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Get the voice file
            voice = update.message.voice
            file = await context.bot.get_file(voice.file_id)
            
            # Download the voice file
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_ogg:
                ogg_path = temp_ogg.name
                await file.download_to_drive(ogg_path)
            
            # Convert OGG to WAV for better processing
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                wav_path = temp_wav.name
                if not self.ai_service.convert_ogg_to_wav(ogg_path, wav_path):
                    await update.message.reply_text("Sorry, I couldn't process the audio file. Please try again.")
                    return
            
            # Use ElevenLabs speech-to-speech
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_mp3:
                mp3_path = temp_mp3.name
                
                # Complete speech-to-speech pipeline
                ai_response = self.ai_service.speech_to_speech(wav_path, mp3_path)
                
                if ai_response:
                    # Send the transcribed text
                    user_message = self.ai_service.speech_to_text(wav_path)
                    await update.message.reply_text(f"🎤 You said: {user_message}")
                    
                    # Send text response
                    await update.message.reply_text(ai_response)
                    
                    # Send voice response
                    with open(mp3_path, 'rb') as audio_file:
                        await context.bot.send_audio(
                            chat_id=update.effective_chat.id,
                            audio=audio_file,
                            title="AI Voice Response",
                            performer="AI Assistant (ElevenLabs)"
                        )
                else:
                    await update.message.reply_text("Sorry, I couldn't process your voice message. Please try again.")
            
            # Clean up temporary files
            os.unlink(ogg_path)
            os.unlink(wav_path)
            if os.path.exists(mp3_path):
                os.unlink(mp3_path)
                
        except Exception as e:
            logger.error(f"Error handling voice message: {e}")
            await update.message.reply_text("Sorry, I encountered an error while processing your voice message. Please try again.")
    
    async def handle_audio_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle audio messages using ElevenLabs speech-to-speech."""
        user_id = update.effective_user.id
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Get the audio file
            audio = update.message.audio
            file = await context.bot.get_file(audio.file_id)
            
            # Download the audio file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
                audio_path = temp_audio.name
                await file.download_to_drive(audio_path)
            
            # Use ElevenLabs speech-to-speech
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_mp3:
                mp3_path = temp_mp3.name
                
                # Complete speech-to-speech pipeline
                ai_response = self.ai_service.speech_to_speech(audio_path, mp3_path)
                
                if ai_response:
                    # Send the transcribed text
                    user_message = self.ai_service.speech_to_text(audio_path)
                    await update.message.reply_text(f"🎵 You said: {user_message}")
                    
                    # Send text response
                    await update.message.reply_text(ai_response)
                    
                    # Send voice response
                    with open(mp3_path, 'rb') as audio_file:
                        await context.bot.send_audio(
                            chat_id=update.effective_chat.id,
                            audio=audio_file,
                            title="AI Voice Response",
                            performer="AI Assistant (ElevenLabs)"
                        )
                else:
                    await update.message.reply_text("Sorry, I couldn't process your audio message. Please try again.")
            
            # Clean up temporary files
            os.unlink(audio_path)
            if os.path.exists(mp3_path):
                os.unlink(mp3_path)
                
        except Exception as e:
            logger.error(f"Error handling audio message: {e}")
            await update.message.reply_text("Sorry, I encountered an error while processing your audio message. Please try again.")
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries from inline buttons."""
        query = update.callback_query
        await query.answer()
        
        if query.data == "search_kb":
            await query.edit_message_text(
                "🔍 **Search the Knowledge Base**\n\n"
                "Use `/search <your query>` to search for specific topics.\n\n"
                "Examples:\n"
                "• `/search machine learning`\n"
                "• `/search neural networks`\n"
                "• `/search AI ethics`"
            )
        
        elif query.data == "history":
            user_id = update.effective_user.id
            history = self.ai_service.get_conversation_history(user_id, limit=3)
            
            if not history:
                await query.edit_message_text("No conversation history found.")
                return
            
            response = "📚 **Your Recent Conversations:**\n\n"
            for i, conv in enumerate(history, 1):
                response += f"**{i}. {conv['timestamp']}**\n"
                response += f"Q: {conv['message'][:80]}...\n"
                response += f"A: {conv['response'][:80]}...\n\n"
            
            await query.edit_message_text(response)
        
        elif query.data == "add_knowledge":
            await query.edit_message_text(
                "➕ **Add Knowledge to Database**\n\n"
                "Please use the format:\n\n"
                "Title: [Your Title]\n"
                "Category: [Category]\n"
                "Tags: [tag1, tag2, tag3]\n"
                "Content: [Your content here]\n\n"
                "Or contact the bot administrator to add knowledge directly to the database."
            )
    
    def run(self):
        """Start the bot."""
        logger.info("Starting Telegram AI Bot...")
        self.application.run_polling()

if __name__ == "__main__":
    bot = TelegramAIBot()
    bot.run()
