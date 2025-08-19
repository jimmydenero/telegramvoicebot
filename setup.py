#!/usr/bin/env python3
"""
Setup script for the Telegram AI Knowledge Bot.
This script helps users set up the bot quickly and easily.
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies. Please run: pip install -r requirements.txt")
        return False

def create_env_file():
    """Create .env file from template."""
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists("env_example.txt"):
        shutil.copy("env_example.txt", ".env")
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your API keys")
        return True
    else:
        print("❌ env_example.txt not found")
        return False

def populate_database():
    """Populate database with sample data."""
    print("\n🗄️  Populating database with sample data...")
    try:
        subprocess.check_call([sys.executable, "sample_data.py"])
        return True
    except subprocess.CalledProcessError:
        print("❌ Error populating database")
        return False

def check_environment():
    """Check if environment variables are set."""
    print("\n🔍 Checking environment variables...")
    
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        return False
    
    # Load environment variables
    with open(".env", "r") as f:
        env_content = f.read()
    
    required_vars = ["TELEGRAM_BOT_TOKEN", "OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if f"{var}=" not in env_content or f"{var}=your_" in env_content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or not configured: {', '.join(missing_vars)}")
        print("Please edit .env file with your actual API keys")
        return False
    
    print("✅ Environment variables configured")
    return True

def main():
    """Main setup function."""
    print("🤖 Telegram AI Knowledge Bot Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        print("\n⚠️  Setup incomplete. Please configure your API keys in .env file")
        print("Then run this script again or start the bot manually.")
        return
    
    # Populate database
    if not populate_database():
        print("⚠️  Database population failed, but you can still run the bot")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Make sure your .env file has correct API keys")
    print("2. Run the bot: python telegram_bot.py")
    print("3. Test the bot in Telegram")
    
    print("\n📚 Available commands:")
    print("• /start - Welcome message")
    print("• /help - Show help")
    print("• /search <query> - Search knowledge base")
    print("• /history - View conversation history")
    
    print("\n🚀 Ready to start! Run: python telegram_bot.py")

if __name__ == "__main__":
    main()
