import supabase
from config import SUPABASE_URL, SUPABASE_KEY
import logging

logger = logging.getLogger(__name__)

class SupabaseDB:
    def __init__(self):
        self.client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
        
    def get_user_chats(self, user_id):
        """Get chat history for a specific user"""
        try:
            response = self.client.table('chats').select('*').eq('user_id', user_id).order('created_at', desc=True)
            return response.data
        except Exception as e:
            logger.error(f"Error getting user chats: {e}")
            return []
    
    def save_chat_message(self, user_id, message_type, content, context=None):
        """Save a chat message to database"""
        try:
            data = {
                'user_id': user_id,
                'message_type': message_type,
                'content': content,
                'context': context or '',
                'created_at': None  # Will be set by Supabase
            }
            
            response = self.client.table('chats').insert(data)
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"Error saving chat message: {e}")
            return None
    
    def get_conversation_context(self, user_id, limit=5):
        """Get conversation context for current chat"""
        try:
            # Get recent messages from the same user
            response = self.client.table('chats').select('message_type, content').eq('user_id', user_id).order('created_at', desc=True).limit(limit)
            messages = response.data
            
            # Format context for AI model
            context = ""
            for msg in messages:
                if msg['message_type'] == 'user':
                    context += f"User: {msg['content']}\n"
                else:
                    context += f"Aura: {msg['content']}\n"
            
            return context
            
        except Exception as e:
            logger.error(f"Error getting conversation context: {e}")
            return ""