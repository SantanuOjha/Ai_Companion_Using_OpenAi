<<<<<<< HEAD
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("Warning: Speech recognition not available due to Python 3.13 compatibility issues")

import pyttsx3
import threading
from config import DEFAULT_VOICE_RATE, DEFAULT_VOICE_VOLUME

class VoiceHandler:
    def __init__(self):
        # Initialize speech recognition if available
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            try:
                self.microphone = sr.Microphone()
                # Adjust for ambient noise
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
            except Exception as e:
                print(f"Warning: Microphone initialization failed: {e}")
                self.microphone = None
        else:
            self.recognizer = None
            self.microphone = None
        
        # Initialize text-to-speech
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', DEFAULT_VOICE_RATE)
            self.tts_engine.setProperty('volume', DEFAULT_VOICE_VOLUME)
        except Exception as e:
            print(f"Warning: Text-to-speech initialization failed: {e}")
            self.tts_engine = None
    
    def listen(self):
        """Listen for voice input and return transcribed text"""
        if not SPEECH_RECOGNITION_AVAILABLE or not self.microphone:
            return "Speech recognition not available on this system."
            
        try:
            print("Listening...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5)
            
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            return "Sorry, I didn't hear anything."
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Sorry, speech recognition service is unavailable."
        except Exception as e:
            return f"Error during speech recognition: {e}"
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"AI: {text}")
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Text-to-speech error: {e}")
        else:
            print("Text-to-speech not available")
    
    def speak_async(self, text):
        """Speak without blocking"""
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.start()
=======
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("Warning: Speech recognition not available due to Python 3.13 compatibility issues")

import pyttsx3
import threading
from config import DEFAULT_VOICE_RATE, DEFAULT_VOICE_VOLUME

class VoiceHandler:
    def __init__(self):
        # Initialize speech recognition if available
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            try:
                self.microphone = sr.Microphone()
                # Adjust for ambient noise
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
            except Exception as e:
                print(f"Warning: Microphone initialization failed: {e}")
                self.microphone = None
        else:
            self.recognizer = None
            self.microphone = None
        
        # Initialize text-to-speech
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', DEFAULT_VOICE_RATE)
            self.tts_engine.setProperty('volume', DEFAULT_VOICE_VOLUME)
        except Exception as e:
            print(f"Warning: Text-to-speech initialization failed: {e}")
            self.tts_engine = None
    
    def listen(self):
        """Listen for voice input and return transcribed text"""
        if not SPEECH_RECOGNITION_AVAILABLE or not self.microphone:
            return "Speech recognition not available on this system."
            
        try:
            print("Listening...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5)
            
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            return "Sorry, I didn't hear anything."
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Sorry, speech recognition service is unavailable."
        except Exception as e:
            return f"Error during speech recognition: {e}"
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"AI: {text}")
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Text-to-speech error: {e}")
        else:
            print("Text-to-speech not available")
    
    def speak_async(self, text):
        """Speak without blocking"""
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.start()
>>>>>>> 44168a780ffe20832cc5b64a57dfbe35a56e354d
        return thread