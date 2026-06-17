"""
YouTube English Learning PDF Generator
Extract subtitles -> Translate to bilingual -> Generate PDF

Usage:
    python main.py <YouTube_URL>
    python main.py   (interactive - will prompt for URL)
"""

import re
import sys
import requests
import os
from dotenv import load_dotenv

from get_transcripts import get_transcript
from translate import translate_transcript
from generate_pdf import generate_pdf

load_dotenv()


def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def get_video_info(video_id):
    """Get video title and channel from YouTube oEmbed API."""
    try:
        resp = requests.get(
            f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json",
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("title", "Unknown"), data.get("author_name", "Unknown")
    except Exception:
        pass
    return "Unknown", "Unknown"


def run(url):
    """Full pipeline: URL -> bilingual PDF."""
    print("=" * 50)
    print("  YouTube English Learning PDF Generator")
    print("=" * 50)

    # Parse URL
    video_id = extract_video_id(url)
    if not video_id:
        print(f"Invalid YouTube URL: {url}")
        return None

    # Get video info
    print(f"\n[1/3] Getting video info...")
    title, channel = get_video_info(video_id)
    print(f"  Title:   {title}")
    print(f"  Channel: {channel}")

    # Get transcript
    print(f"\n[2/3] Extracting transcript...")
    transcript = get_transcript(video_id)
    if not transcript:
        print("  Failed to get transcript. The video may not have subtitles.")
        return None
    print(f"  Got {len(transcript.split())} words")

    # Translate
    print(f"\n[3/3] Translating to bilingual format...")
    pairs = translate_transcript(transcript, title, channel)
    if not pairs:
        print("  Translation failed.")
        return None
    print(f"  Generated {len(pairs)} bilingual pairs")

    # Generate PDF
    print(f"\nGenerating PDF...")
    pdf_path = generate_pdf(pairs, title, channel)
    print(f"\n{'=' * 50}")
    print(f"  Done! PDF saved to:")
    print(f"  {pdf_path}")
    print(f"{'=' * 50}")

    return pdf_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter YouTube URL: ").strip()

    if url:
        run(url)
