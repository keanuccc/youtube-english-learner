"""Translate transcript into bilingual English-Chinese pairs using DeepSeek."""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# Max characters per translation batch
CHUNK_SIZE = 12000


def split_transcript(text, max_chars=CHUNK_SIZE):
    """Split transcript into chunks by sentence boundaries."""
    sentences = []
    current = ""

    for char in text:
        current += char
        if char in ".!?" and len(current) > 50:
            sentences.append(current.strip())
            current = ""

    if current.strip():
        sentences.append(current.strip())

    chunks = []
    chunk = ""
    for s in sentences:
        if len(chunk) + len(s) + 1 > max_chars and chunk:
            chunks.append(chunk.strip())
            chunk = s
        else:
            chunk = chunk + " " + s if chunk else s

    if chunk.strip():
        chunks.append(chunk.strip())

    return chunks


def translate_chunk(text, title, channel):
    """Translate one chunk of transcript into bilingual pairs."""
    prompt = f"""You are a professional bilingual translator for English learners.
Split this video transcript into natural, complete sentences.
For each sentence, provide the English original and Chinese translation.

VIDEO: {title} ({channel})

TRANSCRIPT:
{text}

Format each pair EXACTLY as:
EN: (English sentence)
CN: (Chinese translation)

Rules:
- Split at sentence boundaries (. ! ?)
- Keep each sentence complete and natural
- Fix obvious transcription errors
- Translate naturally, not word-by-word
- One blank line between each pair
- Output ONLY the bilingual pairs, nothing else"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"  Translation error: {e}")
        return None


def parse_bilingual_pairs(text):
    """Parse EN/CN pairs from the translation response."""
    pairs = []
    lines = text.strip().split("\n")
    en_line = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("EN:"):
            en_line = stripped[3:].strip()
        elif stripped.startswith("CN:") and en_line:
            cn_line = stripped[3:].strip()
            pairs.append((en_line, cn_line))
            en_line = None

    return pairs


def translate_transcript(transcript, title, channel):
    """
    Full translation pipeline.
    Returns list of (english, chinese) tuples.
    """
    chunks = split_transcript(transcript)
    print(f"  Translating in {len(chunks)} batch(es)...")

    all_pairs = []
    for i, chunk in enumerate(chunks):
        if len(chunks) > 1:
            print(f"  Batch {i + 1}/{len(chunks)}...")

        result = translate_chunk(chunk, title, channel)
        if result:
            pairs = parse_bilingual_pairs(result)
            all_pairs.extend(pairs)

    return all_pairs
