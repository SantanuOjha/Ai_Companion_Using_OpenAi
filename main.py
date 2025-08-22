from ai_engine.chat_engine import ChatEngine
from voice.voice_handler import VoiceHandler
from ui.web_interface import WebInterface
import os

def main():
    # Initialize components
    chat_engine = ChatEngine()
    voice_handler = VoiceHandler()
    web_interface = WebInterface(chat_engine, voice_handler)
    
    print("AI Companion starting...")
    print("Visit http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop")
    
    # Run the web interface
    web_interface.run()

if __name__ == "__main__":
    main()