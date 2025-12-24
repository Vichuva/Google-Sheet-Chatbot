"""
Voice utilities for ElevenLabs integration.
Provides speech-to-text and text-to-speech functionality.
"""

import os
from elevenlabs.client import ElevenLabs
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key from environment
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio file to text using ElevenLabs Scribe v1.
    
    Args:
        audio_file_path: Path to audio file
        
    Returns:
        Transcribed text
    """
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        # Use Scribe v1 for transcription with explicit English language
        with open(audio_file_path, 'rb') as audio_file:
            # Correct API call for speech-to-text
            result = client.speech_to_text.convert(
                file=audio_file,
                model_id="scribe_v1",
                language_code="en"  # Force English instead of auto-detect
            )
        
        # Extract text from result
        if hasattr(result, 'text'):
            return result.text
        elif isinstance(result, dict):
            return result.get('text', str(result))
        else:
            return str(result)
            
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

def text_to_speech(text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb") -> bytes:
    """
    Convert text to speech using Google TTS (gTTS) with automatic language detection.
    Supports Tamil and English based on the text content.
    
    Args:
        text: Text to convert to speech
        voice_id: Not used with gTTS (kept for compatibility)
        
    Returns:
        Audio bytes
    """
    try:
        # Use gTTS as a free alternative since ElevenLabs free tier is restricted
        from gtts import gTTS
        from langdetect import detect
        import io
        
        # Detect language from text
        try:
            detected_lang = detect(text)
            # Map detected language to gTTS language codes
            if detected_lang == 'ta':  # Tamil
                lang = 'ta'
            elif detected_lang in ['en', 'en-us', 'en-gb']:  # English
                lang = 'en'
            else:
                # Default to English for other languages
                lang = 'en'
        except:
            # If detection fails, default to English
            lang = 'en'
        
        # Create TTS object with detected language
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save to bytes
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        
        return audio_fp.read()
        
    except ImportError as e:
        if 'langdetect' in str(e):
            raise Exception("langdetect not installed. Install with: pip install langdetect")
        else:
            raise Exception("gTTS not installed. Install with: pip install gtts")
    except Exception as e:
        raise Exception(f"Text-to-speech failed: {str(e)}")

def save_audio_temp(audio_bytes: bytes) -> str:
    """
    Save audio bytes to a temporary file.
    
    Args:
        audio_bytes: Audio data
        
    Returns:
        Path to temporary audio file
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_file.write(audio_bytes)
    temp_file.close()
    return temp_file.name
