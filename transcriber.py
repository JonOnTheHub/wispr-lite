from groq import Groq
from config import GROQ_API_KEY, WHISPER_MODEL

client = Groq(api_key=GROQ_API_KEY)

def transcribe(audio_path: str) -> str:
    print("[transcriber] sending to Whisper...")

    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=f,
            response_format="text"
        )

    transcript = result.strip()
    print(f"[transcriber] raw: {transcript}")
    return transcript