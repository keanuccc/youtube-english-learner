"""
Local API server for the YouTube English Learning extension.
Wraps the existing pipeline as REST endpoints.
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
import sys
import os

sys.path.insert(0, str(Path(__file__).parent))

from get_transcripts import get_transcript
from translate import translate_transcript
from generate_pdf import generate_pdf
from main import extract_video_id, get_video_info

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
CORS(app)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        title, channel = get_video_info(video_id)

        transcript = get_transcript(video_id)
        if not transcript:
            return jsonify({"error": "No subtitles found for this video"}), 404

        pairs = translate_transcript(transcript, title, channel)
        if not pairs:
            return jsonify({"error": "Translation failed"}), 500

        pdf_path = generate_pdf(pairs, title, channel)

        return jsonify({
            "title": title,
            "channel": channel,
            "word_count": len(transcript.split()),
            "pair_count": len(pairs),
            "pdf": os.path.basename(pdf_path),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/download/<filename>", methods=["GET"])
def download(filename):
    filepath = OUTPUT_DIR / filename
    if not filepath.exists():
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath, as_attachment=True)


@app.route("/api/history", methods=["GET"])
def history():
    pdfs = sorted(OUTPUT_DIR.glob("*.pdf"), key=os.path.getmtime, reverse=True)
    items = []
    for pdf in pdfs[:20]:
        from datetime import datetime
        stat = pdf.stat()
        items.append({
            "name": pdf.name,
            "size": round(stat.st_size / 1024),
            "time": datetime.fromtimestamp(stat.st_mtime).strftime("%m/%d %H:%M"),
        })
    return jsonify(items)


if __name__ == "__main__":
    print("YouTube English Learning API Server")
    print("http://localhost:5000")
    print("Press Ctrl+C to stop")
    app.run(host="127.0.0.1", port=5000, debug=False)
