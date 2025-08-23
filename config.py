<<<<<<< HEAD
import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'your-google-api-key-here')

# Clerk Authentication
CLERK_PUBLISHABLE_KEY = os.getenv('CLERK_PUBLISHABLE_KEY', 'your-clerk-publishable-key')
CLERK_SECRET_KEY = os.getenv('CLERK_SECRET_KEY', 'your-clerk-secret-key')
CLERK_JWKS_URL = f"https://clerk.your-instance.clerk.accounts.dev/.well-known/jwks.json"

# Supabase Database
SUPABASE_URL = os.getenv('SUPABASE_URL', 'your-supabase-url')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'your-supabase-key')

COMPANION_PERSONALITY = """
You are Aura, a friendly and intelligent AI companion. Your personality traits:
- You're genuinely interested in the user's thoughts and feelings
- You provide thoughtful advice when asked
- You can be playful and humorous when appropriate
- You remember previous conversations across sessions
- You admit when you don't know something
- You're helpful, patient, and engaging

Always respond in a conversational, natural way. Keep responses concise but informative.
"""

DEFAULT_VOICE_RATE = 200
=======
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
>>>>>>> 44168a780ffe20832cc5b64a57dfbe35a56e354d
DEFAULT_VOICE_VOLUME = 0.9