<<<<<<< HEAD
import google.generativeai as genai
from config import GOOGLE_API_KEY, COMPANION_PERSONALITY
from database.supabase_db import SupabaseDB
import logging

logger = logging.getLogger(__name__)

class ChatEngine:
    def __init__(self, db=None):
        self.use_mock = False
        self.db = db or SupabaseDB()
        self.conversation_history = []
        
        # Configure Gemini
        if GOOGLE_API_KEY and GOOGLE_API_KEY != 'your-google-api-key-here':
            try:
                genai.configure(api_key=GOOGLE_API_KEY)
                self.model = genai.GenerativeModel('gemini-pro')
                # Test connection
                test_prompt = "Respond with 'OK' only"
                response = self.model.generate_content(test_prompt)
                if response.text:
                    logger.info("Google Gemini API connected successfully")
                else:
                    raise Exception("Empty response from API")
            except Exception as e:
                logger.error(f"Gemini API connection failed: {e}")
                self.use_mock = True
        else:
            logger.warning("No valid Google API key found. Using mock mode.")
            self.use_mock = True
    
    def get_mock_response(self, user_message):
        """Enhanced mock responses"""
        user_message = user_message.lower()
        
        if any(word in user_message for word in ['weather', 'temperature', 'rain', 'sun']):
            return "I don't have access to real-time weather data, but I'd be happy to help you find weather information or discuss weather patterns!"
        
        if any(word in user_message for word in ['time', 'clock', 'hour']):
            return "I don't have access to real-time clock data, but you can check your device for the current time."
        
        if any(word in user_message for word in ['name', 'who are you']):
            return "I'm Aura, your AI companion! I'm here to chat, help with questions, and be a friendly presence."
        
        if any(word in user_message for word in ['hello', 'hi', 'hey']):
            return "Hello there! I'm Aura, your AI companion. How can I help you today?"
        
        if 'help' in user_message:
            return "I can chat with you, answer questions, help with creative tasks, and more! Try asking me about anything you're curious about."
        
        if any(word in user_message for word in ['bye', 'goodbye', 'see you']):
            return "Goodbye! Feel free to come back anytime you want to chat. I'll be here!"
        
        # Default response
        return "I'm Aura, your AI companion! I'm here to have a meaningful conversation with you. What would you like to talk about?"
    
    def get_response(self, user_message, user_id=None):
        """Generate response with context awareness"""
        if self.use_mock:
            return self.get_mock_response(user_message)
        
        try:
            # Get conversation context from database
            context = ""
            if user_id:
                context = self.db.get_conversation_context(user_id)
            
            # Build prompt with personality and context
            prompt = f"""
{COMPANION_PERSONALITY}

Conversation context:
{context}

User: {user_message}
Aura:"""
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response.text:
                ai_response = response.text.strip()
                
                # Save messages to database
                if user_id:
                    self.db.save_chat_message(user_id, 'user', user_message)
                    self.db.save_chat_message(user_id, 'assistant', ai_response)
                
                return ai_response
            else:
                return "I'm having trouble formulating a response right now. Could you try asking again?"
                
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return "Sorry, I'm experiencing some technical difficulties. Let's continue our conversation!"
    
    def clear_history(self):
        self.conversation_history = []
    
    def get_history(self, user_id):
        """Get chat history for user"""
        return self.db.get_user_chats(user_id)
=======
import google.generativeai as genai
from config import GOOGLE_API_KEY, COMPANION_PERSONALITY
import os
import logging

logger = logging.getLogger(__name__)

class ChatEngine:
    def __init__(self):
        self.use_mock = False
        self.conversation_history = []
        
        # Check if API key is valid
        if not GOOGLE_API_KEY or GOOGLE_API_KEY == 'your-google-api-key-here':
            logger.warning("No valid Google API key found. Using mock mode.")
            self.use_mock = True
        else:
            try:
                genai.configure(api_key=GOOGLE_API_KEY)
                # Set up the model
                self.model = genai.GenerativeModel('gemini-pro')
                # Test the connection
                test_response = self.model.generate_content("Hello, test connection")
                logger.info("Google Gemini API connection successful")
            except Exception as e:
                logger.error(f"Google Gemini API connection failed: {e}")
                self.use_mock = True
    
    def get_mock_response(self, user_message):
        """Mock response for testing without API key"""
        mock_responses = {
            "hello": "Hello there! I'm Aura, your AI companion. How can I help you today?",
            "hi": "Hi! Nice to meet you! What would you like to talk about?",
            "how are you": "I'm doing great, thank you for asking! I'm here and ready to help.",
            "what can you do": "I can chat with you, answer questions, help with creative tasks, and more! Try asking me something.",
            "bye": "Goodbye! Feel free to come back anytime you want to chat.",
            "help": "I'm here to be your companion! You can chat with me through text or voice. What would you like to do?"
        }
        
        # Return specific response or default
        for key, response in mock_responses.items():
            if key in user_message.lower():
                return response
        
        return "I'm your AI companion Aura! I'm here to chat and help. Tell me more about what you'd like to discuss."
    
    def format_history_for_gemini(self):
        """Format conversation history for Gemini API"""
        formatted_history = []
        for message in self.conversation_history:
            if message["role"] == "user":
                formatted_history.append(f"User: {message['content']}")
            elif message["role"] == "assistant":
                formatted_history.append(f"Aura: {message['content']}")
        return "\n".join(formatted_history)
    
    def get_response(self, user_message):
        # Add user message to history
        self.conversation_history.append({
            "role": "user", 
            "content": user_message
        })
        
        if self.use_mock:
            response_text = self.get_mock_response(user_message)
        else:
            try:
                # Format the conversation history
                history_text = self.format_history_for_gemini()
                
                # Create prompt with personality
                prompt = f"""
{COMPANION_PERSONALITY}

Conversation history:
{history_text}

User: {user_message}
Aura:"""
                
                # Get AI response
                response = self.model.generate_content(prompt)
                response_text = response.text.strip()
                
            except Exception as e:
                logger.error(f"Google Gemini API error: {e}")
                response_text = "Sorry, I'm having trouble responding right now. Let's continue our chat!"
        
        # Add AI response to history
        self.conversation_history.append({
            "role": "assistant", 
            "content": response_text
        })
        
        return response_text
    
    def clear_history(self):
        self.conversation_history = []
>>>>>>> 44168a780ffe20832cc5b64a57dfbe35a56e354d
