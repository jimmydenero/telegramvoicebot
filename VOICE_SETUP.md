# 🎤 Voice-to-Voice Setup Guide

This guide explains how to set up and use the voice-to-voice functionality in your Telegram AI Bot using ElevenLabs.

## 🚀 Quick Setup

### 1. Get ElevenLabs API Key

1. Go to [ElevenLabs Platform](https://elevenlabs.io/)
2. Sign up for a free account
3. Navigate to your profile settings
4. Copy your API key

### 2. Configure Environment

Add your ElevenLabs API key to your `.env` file:

```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### 3. Test the Setup

Run the test script to verify everything works:

```bash
python3 test_elevenlabs.py
```

## 🎯 How It Works

The voice-to-voice feature uses a complete pipeline:

1. **Voice Input**: User sends a voice message to the bot
2. **Speech-to-Text**: OpenAI Whisper converts speech to text
3. **AI Processing**: ChatGPT generates a response
4. **Text-to-Speech**: ElevenLabs converts the response to natural speech
5. **Voice Output**: Bot sends back an audio response

## 🎤 Available Voices

Use the `/voices` command in your bot to see all available ElevenLabs voices.

### Popular Voices:
- **Rachel** (ID: `21m00Tcm4TlvDq8ikWAM`) - Default voice
- **Domi** (ID: `AZnzlk1XvdvUeBnXmlld`) - Professional female
- **Bella** (ID: `EXAVITQu4vr4xnSDxMaL`) - Warm female
- **Antoni** (ID: `ErXwobaYiN019PkySvjV`) - Professional male
- **Josh** (ID: `TxGEqnHWrfWFTfGW9XjX`) - Casual male

## 🔧 Customization

### Change Default Voice

Edit the `voice_id` parameter in `ai_service.py`:

```python
def text_to_speech(self, text: str, output_path: str, voice_id: str = "YOUR_PREFERRED_VOICE_ID") -> bool:
```

### Voice Settings

You can customize voice characteristics:

```python
from elevenlabs import Voice, VoiceSettings

voice_settings = VoiceSettings(
    stability=0.5,
    similarity_boost=0.5,
    style=0.0,
    use_speaker_boost=True
)
```

## 💰 Pricing

- **Free Tier**: 10,000 characters per month
- **Paid Plans**: Starting at $22/month for 30,000 characters
- **Enterprise**: Custom pricing for high-volume usage

## 🛠️ Troubleshooting

### Common Issues

1. **"API key not found"**
   - Check your `.env` file has the correct API key
   - Restart the bot after adding the key

2. **"Voice generation failed"**
   - Check your ElevenLabs account has available characters
   - Verify the voice ID is correct

3. **"Audio file processing error"**
   - Ensure FFmpeg is installed: `brew install ffmpeg`
   - Check file permissions in the temp directory

### Testing

Use the test script to verify each component:

```bash
python3 test_elevenlabs.py
```

## 🎉 Usage

Once set up, simply:

1. Start your bot: `python3 telegram_bot.py`
2. Send a voice message to your bot
3. Receive both text and voice responses!

The bot will:
- Show what you said (transcription)
- Provide a text response
- Send a natural-sounding voice response

## 📱 Supported Formats

- **Voice Messages**: Telegram's native voice format
- **Audio Files**: MP3, WAV, OGG, and other common formats
- **Text Messages**: Still fully supported

## 🔒 Privacy

- Voice files are processed temporarily and deleted
- No voice data is stored permanently
- All processing happens through secure APIs
