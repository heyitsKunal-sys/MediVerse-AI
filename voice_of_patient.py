from dotenv import load_dotenv
load_dotenv()

import os
from groq import Groq

# API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Whisper Model
stt_model = "whisper-large-v3"


def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    """
    Transcribe audio using Groq Whisper.
    
    Args:
        stt_model (str): Whisper model name
        audio_filepath (str): Path to audio file
        GROQ_API_KEY (str): Groq API Key

    Returns:
        str: Transcribed text
    """

    try:
        client = Groq(api_key=GROQ_API_KEY)

        with open(audio_filepath, "rb") as audio_file:

            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )

        return transcription.text

    except Exception as e:
        return f"Transcription Error: {str(e)}"