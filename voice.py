import os
import uuid
import speech_recognition as sr
from modules.utils import TEMP_DIR

def transcribe_audio_bytes(audio_bytes: bytes) -> str:
    """
    Converts audio byte data from the browser microphone into text using SpeechRecognition.
    Saves the data to a temporary WAV file, records it withsr.AudioFile,
    and transcribes it using Google Speech Recognition API.
    """
    if not audio_bytes:
        return ""

    # Generate a unique temp path to avoid collisions
    temp_filename = f"recording_{uuid.uuid4().hex}.wav"
    temp_filepath = os.path.join(TEMP_DIR, temp_filename)

    try:
        # Save the audio bytes to a local WAV file
        with open(temp_filepath, "wb") as f:
            f.write(audio_bytes)

        recognizer = sr.Recognizer()

        # Open the audio file using SpeechRecognition
        with sr.AudioFile(temp_filepath) as source:
            # Adjust for ambient noise and record
            audio_data = recognizer.record(source)

        # Transcribe using Google's free API wrapper
        text = recognizer.recognize_google(audio_data)
        return text

    except sr.UnknownValueError:
        raise Exception("Google Speech Recognition could not understand the audio. Please speak clearly.")
    except sr.RequestError as e:
        raise Exception(f"Google Speech Recognition service request failed: {e}. Check your internet connection.")
    except Exception as e:
        raise Exception(f"An error occurred during voice transcription: {str(e)}")
    finally:
        # Ensure temporary file cleanup
        if os.path.exists(temp_filepath):
            try:
                os.remove(temp_filepath)
            except Exception:
                pass
