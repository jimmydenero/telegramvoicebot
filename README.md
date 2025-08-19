# 🤖 Telegram AI Knowledge Bot

A powerful Telegram bot that combines ChatGPT with a custom AI knowledge database to provide intelligent responses about artificial intelligence topics.

## ✨ Features

- **🤖 ChatGPT Integration**: Powered by OpenAI's GPT models for intelligent responses
- **📚 Knowledge Database**: Custom SQLite database with AI knowledge
- **🔍 Smart Search**: Search through the knowledge database for specific topics
- **💬 Conversation History**: Track user interactions and conversation history
- **📝 Knowledge Management**: Add new knowledge to the database
- **🎯 Interactive UI**: Inline buttons and user-friendly commands
- **🎤 Voice-to-Voice Chat**: Send voice messages and get voice responses
- **🔒 Privacy**: Local database storage for conversation history

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key (from [OpenAI Platform](https://platform.openai.com/))
- ElevenLabs API Key (from [ElevenLabs Platform](https://elevenlabs.io/)) - for voice features
- FFmpeg (for audio processing) - Install with `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Ubuntu)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` file with your credentials:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   DATABASE_PATH=./ai_knowledge.db
   MAX_TOKENS=1000
   TEMPERATURE=0.7
   ```

4. **Populate the database with sample data**
   ```bash
   python sample_data.py
   ```

5. **Run the bot**
   ```bash
   python telegram_bot.py
   ```

## 📋 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and main menu |
| `/help` | Show help information |
| `/search <query>` | Search the AI knowledge database |
| `/history` | View your conversation history |
| `/add_knowledge` | Add new knowledge to the database |
| `/voices` | List available ElevenLabs voices |

## 🗂️ Project Structure

```
telegram-ai-bot/
├── telegram_bot.py      # Main bot application
├── ai_service.py        # AI service with ChatGPT integration
├── database.py          # Database management and operations
├── sample_data.py       # Sample data population script
├── requirements.txt     # Python dependencies
├── env_example.txt      # Environment variables template
├── README.md           # This file
└── ai_knowledge.db     # SQLite database (created automatically)
```

## 🔧 Configuration

### Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: GPT model to use (default: gpt-4)
- `ELEVENLABS_API_KEY`: ElevenLabs API key for voice features
- `DATABASE_PATH`: Path to SQLite database file
- `MAX_TOKENS`: Maximum tokens for AI responses
- `TEMPERATURE`: AI response creativity (0.0-1.0)

### Database Schema

The bot uses two main tables:

1. **ai_knowledge**: Stores AI knowledge entries
   - id, title, content, category, tags, created_at, updated_at

2. **conversation_history**: Stores user conversations
   - id, user_id, message, response, timestamp

## 🎯 Usage Examples

### Basic Questions
Users can ask any AI-related question:
- "What is machine learning?"
- "How do neural networks work?"
- "Explain deep learning"

### Voice Messages
- Send voice messages to ask questions
- Get both text and voice responses
- Supports both voice messages and audio files
- Uses ElevenLabs for natural, high-quality voice synthesis
- Multiple voice options available via `/voices` command

### Search Commands
- `/search machine learning`
- `/search neural networks`
- `/search AI ethics`

### View History
- `/history` - Shows recent conversations

## 🔒 Security & Privacy

- **Local Database**: All conversation history is stored locally
- **No Data Sharing**: User data is not shared with third parties
- **API Keys**: Store securely in environment variables
- **Access Control**: Bot can be restricted to specific groups/users

## 🛠️ Customization

### Adding Custom Knowledge

1. **Via Code**:
   ```python
   from database import AIKnowledgeDatabase
   
   db = AIKnowledgeDatabase()
   db.add_knowledge(
       title="Your Title",
       content="Your content here",
       category="Your Category",
       tags=["tag1", "tag2", "tag3"]
   )
   ```

2. **Via Bot**: Use the `/add_knowledge` command

### Modifying AI Behavior

Edit the system prompt in `ai_service.py` to change how the AI responds:

```python
system_prompt = """Your custom system prompt here..."""
```

### Adding New Commands

Add new command handlers in `telegram_bot.py`:

```python
self.application.add_handler(CommandHandler("your_command", self.your_command_handler))
```

## 🚨 Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check if bot token is correct
   - Verify OpenAI API key is valid
   - Check internet connection

2. **Database errors**
   - Ensure write permissions in the directory
   - Check if database file is corrupted

3. **Import errors**
   - Install all requirements: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

### Logs

The bot logs all activities. Check the console output for error messages and debugging information.

## 📈 Future Enhancements

- [ ] Web interface for knowledge management
- [ ] Multi-language support
- [x] Voice message support (implemented with ElevenLabs)
- [ ] Image analysis capabilities
- [ ] Advanced search filters
- [ ] User authentication and roles
- [ ] Analytics dashboard
- [ ] Backup and restore functionality
- [ ] Custom voice cloning
- [ ] Voice emotion detection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section
2. Review the logs for error messages
3. Ensure all dependencies are installed
4. Verify your API keys are correct

---

**Happy coding! 🤖✨**
