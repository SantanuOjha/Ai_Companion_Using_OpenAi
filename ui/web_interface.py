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