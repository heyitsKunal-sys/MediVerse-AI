import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# Load .env file
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


def text_to_speech(text, output_file="doctor_voice.mp3"):

    client = ElevenLabs(
        api_key=ELEVENLABS_API_KEY
    )

    audio_stream = client.text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb",   # George
        model_id="eleven_multilingual_v2",
        text=text,
        output_format="mp3_44100_128"
    )

    # Save audio
    with open(output_file, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    print(f"Audio saved to: {output_file}")

    # IMPORTANT FOR GRADIO
    return output_file


# Test
if __name__ == "__main__":

    text = """
    Hello Kunal.
    I am your AI medical assistant.
    How can I help you today?
    """

    audio_path = text_to_speech(text)

    print(audio_path)