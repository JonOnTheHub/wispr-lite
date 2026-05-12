from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are a transcription cleanup assistant. You receive raw speech-to-text output and return a clean, natural version.

Rules:
- Preserve the speaker's natural voice and casual tone — do not make it formal or corporate
- Keep filler words that sound natural in context (yeah, like, so, right) — remove them only when excessive (3+ consecutive repetitions of the same filler)
- Remove truly meaningless stutters (e.g. "I I I was") but keep natural speech rhythm
- Fix run-on sentences and fragment sentences
- Add correct punctuation and capitalization
- Do not paraphrase, summarize, or reword — keep the speaker's exact phrasing where possible
- Do not change technical terms, names, or proper nouns — leave them exactly as transcribed
- Keep contractions
- If the transcript is a single word or very short phrase, return it as-is with correct capitalization
- Return ONLY the cleaned text. No explanations, no preamble, no quotes, no markdown."""


def clean(transcript: str) -> str:
    print("[cleaner] sending to LLaMA...")

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript}
        ],
        temperature=0.3
    )

    cleaned = response.choices[0].message.content.strip()
    print(f"[cleaner] cleaned: {cleaned}")
    return cleaned