<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from auth.clerk_auth import ClerkAuth
from ai_engine.chat_engine import ChatEngine
from database.supabase_db import SupabaseDB
from voice.voice_handler import VoiceHandler
from config import CLERK_PUBLISHABLE_KEY

class WebInterface:
    def __init__(self):
        self.app = Flask(__name__, 
                        template_folder='../templates',
                        static_folder='../static')
        self.app.config['SECRET_KEY'] = 'your-secret-key-change-this'
        self.app.config['CLERK_PUBLISHABLE_KEY'] = CLERK_PUBLISHABLE_KEY
        
        # Initialize components
        self.auth = ClerkAuth()
        self.db = SupabaseDB()
        self.chat_engine = ChatEngine(self.db)
        self.voice_handler = VoiceHandler()
        
        # Set up routes
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/')
        def index():
            # Check authentication
            user_id = self.auth.verify_user()
            if not user_id:
                return redirect('/login')
            
            return render_template('index.html', config={'CLERK_PUBLISHABLE_KEY': CLERK_PUBLISHABLE_KEY})
        
        @self.app.route('/login')
        def login():
            return render_template('login.html', config={'CLERK_PUBLISHABLE_KEY': CLERK_PUBLISHABLE_KEY})
        
        @self.app.route('/chat', methods=['POST'])
        @self.auth.login_required
        def chat():
            try:
                data = request.get_json()
                user_message = data.get('message', '').strip()
                
                if not user_message:
                    return jsonify({'response': 'Please enter a message.'})
                
                # Get user ID from session
                user_id = session['user_id']
                
                # Get response
                response = self.chat_engine.get_response(user_message, user_id)
                return jsonify({'response': response})
                
            except Exception as e:
                return jsonify({'response': f'Sorry, I encountered an error: {str(e)}'})
        
        @self.app.route('/voice_chat', methods=['POST'])
        @self.auth.login_required
        def voice_chat():
            try:
                user_id = session['user_id']
                
                # Listen for voice input
                user_message = self.voice_handler.listen()
                
                if user_message.startswith("Sorry") or user_message == "Voice recognition is not available.":
                    return jsonify({
                        'user_input': '',
                        'response': user_message
                    })
                
                # Get response
                response = self.chat_engine.get_response(user_message, user_id)
                
                # Speak the response
                self.voice_handler.speak_async(response)
                
                return jsonify({
                    'user_input': user_message,
                    'response': response
                })
                
            except Exception as e:
                return jsonify({
                    'user_input': '',
                    'response': f'Voice chat error: {str(e)}'
                })
        
        @self.app.route('/history', methods=['GET'])
        @self.auth.login_required
        def get_history():
            try:
                user_id = session['user_id']
                history = self.chat_engine.get_history(user_id)
                return jsonify({'history': history})
            except Exception as e:
                return jsonify({'error': str(e)})
        
        @self.app.route('/clear_history', methods=['POST'])
        @self.auth.login_required
        def clear_history():
            try:
                user_id = session['user_id']
                # Clear from database
                self.db.client.table('chats').delete().eq('user_id', user_id)
                return jsonify({'success': True})
            except Exception as e:
                return jsonify({'error': str(e)})
=======
from flask import Flask, render_template, request, jsonify
import json
import os

class WebInterface:
    def __init__(self, chat_engine, voice_handler):
        # Get the project root directory (parent of ui directory)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        template_dir = os.path.join(project_root, 'templates')
        
        self.app = Flask(__name__, template_folder=template_dir)
        self.chat_engine = chat_engine
        self.voice_handler = voice_handler
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        @self.app.route('/chat', methods=['POST'])
        def chat():
            user_message = request.json.get('message', '')
            if user_message:
                response = self.chat_engine.get_response(user_message)
                return jsonify({'response': response})
            return jsonify({'response': 'Please enter a message.'})
        
        @self.app.route('/voice_chat', methods=['POST'])
        def voice_chat():
            # Listen for voice input
            user_message = self.voice_handler.listen()
            if user_message and not user_message.startswith("Sorry"):
                response = self.chat_engine.get_response(user_message)
                # Speak the response
                self.voice_handler.speak_async(response)
                return jsonify({
                    'user_input': user_message,
                    'response': response
                })
            return jsonify({
                'user_input': user_message,
                'response': 'I could not process your voice input.'
            })
    
    def run(self, host='localhost', port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)
>>>>>>> 44168a780ffe20832cc5b64a57dfbe35a56e354d
