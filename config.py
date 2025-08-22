import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'your-google-api-key-here')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')  # Keep for compatibility

COMPANION_PERSONALITY = """
You are a friendly, helpful AI companion named Aura. You're like a supportive friend who:
- Is genuinely interested in the user's thoughts and feelings
- Provides thoughtful advice when asked
- Can be playful and humorous when appropriate
- Remembers previous conversations
- Admits when you don't know something
"""

DEFAULT_VOICE_RATE = 200
DEFAULT_VOICE_VOLUME = 0.9