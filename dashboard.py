"""
YouTube English Learning - Web Dashboard
Beautiful, magazine-style interface for generating bilingual PDFs.
"""

import streamlit as st
import os
from pathlib import Path
from datetime import datetime

from get_transcripts import get_transcript
from translate import translate_transcript
from generate_pdf import generate_pdf
from main import extract_video_id, get_video_info

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ========== Page Config ==========
st.set_page_config(
    page_title="YouTube English Learner",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ========== Custom CSS ==========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ---------- Global ---------- */
.stApp {
    background: #f5f5f7;
    font-family: 'Inter', -apple-system, sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}

/* ---------- Main container ---------- */
.block-container {
    max-width: 720px !important;
    padding-top: 3rem !important;
    padding-bottom: 2rem;
}

/* ---------- Hero ---------- */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.hero-icon {
    font-size: 3.2rem;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 16px rgba(234, 179, 8, 0.25));
}
.hero h1 {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    color: #1a1a1a;
    margin: 0;
    letter-spacing: -0.03em;
}
.hero p {
    color: #888;
    font-size: 0.95rem;
    margin-top: 0.5rem;
    font-weight: 400;
}

/* ---------- Input card ---------- */
.input-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.8rem;
    margin: 1rem 0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

/* Style the text input */
.stTextInput > div > div > input {
    background: #f9fafb !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 12px !important;
    padding: 0.85rem 1.1rem !important;
    font-size: 0.95rem !important;
    color: #1a1a1a !important;
    font-family: 'JetBrains Mono', monospace !important;
    transition: border-color 0.2s ease;
}
.stTextInput > div > div > input:focus {
    border-color: #eab308 !important;
    box-shadow: 0 0 0 3px rgba(234, 179, 8, 0.12) !important;
    background: #ffffff !important;
}
.stTextInput > div > div > input::placeholder {
    color: #b0b0b0 !important;
}

/* Generate button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #eab308 0%, #d97706 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    letter-spacing: 0.02em;
    transition: all 0.2s ease;
    box-shadow: 0 2px 12px rgba(234, 179, 8, 0.25);
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(234, 179, 8, 0.35) !important;
}

/* ---------- Progress section ---------- */
.progress-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.progress-title {
    color: #374151;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
}

/* Step indicators */
.steps {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    flex-wrap: wrap;
}
.step {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 500;
    transition: all 0.3s ease;
}
.step-pending {
    background: #f3f4f6;
    color: #9ca3af;
    border: 1px solid #e5e7eb;
}
.step-active {
    background: rgba(234, 179, 8, 0.1);
    color: #b45309;
    border: 1px solid rgba(234, 179, 8, 0.4);
    animation: pulse-glow 1.5s ease-in-out infinite;
}
.step-done {
    background: rgba(34, 197, 94, 0.1);
    color: #16a34a;
    border: 1px solid rgba(34, 197, 94, 0.3);
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(234, 179, 8, 0); }
    50% { box-shadow: 0 0 12px 2px rgba(234, 179, 8, 0.12); }
}

/* Spinner override */
.stSpinner > div {
    border-top-color: #eab308 !important;
}

/* ---------- Result card ---------- */
.result-card {
    background: #ffffff;
    border: 1px solid #d1fae5;
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 2px 12px rgba(34, 197, 94, 0.08);
    animation: fade-in 0.4s ease;
}
@keyframes fade-in {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.result-title {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1.2rem;
    color: #1a1a1a;
    margin-bottom: 0.3rem;
    line-height: 1.4;
}
.result-channel {
    color: #6b7280;
    font-size: 0.85rem;
    margin-bottom: 1.2rem;
}

/* Stats row */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.stat-box {
    flex: 1;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #d97706;
}
.stat-label {
    font-size: 0.7rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    letter-spacing: 0.02em;
    box-shadow: 0 2px 12px rgba(34, 197, 94, 0.2);
}
.stDownloadButton > button:hover {
    box-shadow: 0 4px 20px rgba(34, 197, 94, 0.3) !important;
}

/* ---------- History section ---------- */
.history-header {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: #6b7280;
    margin: 2rem 0 1rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e5e7eb;
    letter-spacing: 0.02em;
}
.history-empty {
    color: #c0c0c0;
    font-size: 0.85rem;
    text-align: center;
    padding: 2rem 0;
}
.history-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.75rem 1rem;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.history-item:hover {
    border-color: #d1d5db;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.history-icon {
    font-size: 1.3rem;
    flex-shrink: 0;
}
.history-info {
    flex: 1;
    min-width: 0;
}
.history-name {
    font-size: 0.8rem;
    font-weight: 500;
    color: #374151;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.history-meta {
    font-size: 0.7rem;
    color: #9ca3af;
    margin-top: 0.15rem;
}

/* ---------- Divider ---------- */
.divider {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 1.5rem 0;
}

/* ---------- Error card ---------- */
.error-card {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
    color: #dc2626;
    font-size: 0.9rem;
}

/* ---------- Warning text ---------- */
.stAlert > div {
    border-radius: 10px !important;
    font-size: 0.9rem !important;
}
</style>
""", unsafe_allow_html=True)

# ========== Session State ==========
if "processing" not in st.session_state:
    st.session_state.processing = False
if "step" not in st.session_state:
    st.session_state.step = 0
if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error = None

# ========== Helper: PDF history ==========
def get_pdf_history():
    pdfs = sorted(OUTPUT_DIR.glob("*.pdf"), key=os.path.getmtime, reverse=True)
    items = []
    for pdf in pdfs[:20]:
        stat = pdf.stat()
        items.append({
            "name": pdf.name,
            "path": str(pdf),
            "size": stat.st_size / 1024,
            "time": datetime.fromtimestamp(stat.st_mtime),
        })
    return items

# ========== Helper: step display ==========
def render_steps(current_step):
    labels = ["📝 Extract", "🌐 Translate", "📄 PDF"]
    icons = ["", "", ""]
    html = '<div class="steps">'
    for i, (label, icon) in enumerate(zip(labels, icons)):
        if i < current_step:
            cls = "step-done"
            badge = "✓"
        elif i == current_step:
            cls = "step-active"
            badge = icon
        else:
            cls = "step-pending"
            badge = "○"
        html += f'<div class="step {cls}">{badge} {label}</div>'
    html += '</div>'
    return html

# ========== Pipeline ==========
def run_pipeline(url):
    try:
        # Step 0: Extract
        st.session_state.step = 0

        video_id = extract_video_id(url)
        if not video_id:
            raise ValueError(f"Invalid YouTube URL")

        title, channel = get_video_info(video_id)

        transcript = get_transcript(video_id)
        if not transcript:
            raise ValueError("No subtitles found. Video may not have subtitles.")

        # Step 1: Translate
        st.session_state.step = 1

        pairs = translate_transcript(transcript, title, channel)
        if not pairs:
            raise ValueError("Translation failed.")

        # Step 2: Generate PDF
        st.session_state.step = 2

        pdf_path = generate_pdf(pairs, title, channel)

        st.session_state.result = {
            "title": title,
            "channel": channel,
            "word_count": len(transcript.split()),
            "pair_count": len(pairs),
            "pdf_path": pdf_path,
        }
        st.session_state.processing = False
        st.rerun()

    except Exception as e:
        st.session_state.error = str(e)
        st.session_state.processing = False
        st.rerun()

# ========== Process if needed ==========
if st.session_state.processing:
    st.markdown("""
    <div class="progress-card">
        <div class="progress-title">Processing your video...</div>
    """, unsafe_allow_html=True)

    st.markdown(render_steps(st.session_state.step), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    run_pipeline(st.session_state.get("url", ""))

# ========== Hero ==========
st.markdown("""
<div class="hero">
    <div class="hero-icon">📚</div>
    <h1>YouTube English Learner</h1>
    <p>Paste a YouTube link → Get a bilingual PDF for note-taking</p>
</div>
""", unsafe_allow_html=True)

# ========== Input Card ==========
st.markdown('<div class="input-card">', unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1.2])

with col_input:
    url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
    )

with col_btn:
    generate_clicked = st.button(
        "⚡ Generate",
        type="primary",
        use_container_width=True,
    )

st.markdown('</div>', unsafe_allow_html=True)

if generate_clicked:
    if not url.strip():
        st.warning("Please paste a YouTube URL first.")
    else:
        st.session_state.url = url.strip()
        st.session_state.processing = True
        st.session_state.result = None
        st.session_state.error = None
        st.session_state.step = 0
        st.rerun()

# ========== Error ==========
if st.session_state.error:
    st.markdown(f'<div class="error-card">⚠️ {st.session_state.error}</div>', unsafe_allow_html=True)
    st.session_state.error = None

# ========== Result ==========
if st.session_state.result:
    r = st.session_state.result
    pdf_name = os.path.basename(r["pdf_path"])

    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">✅ {r['title']}</div>
        <div class="result-channel">{r['channel']}</div>
        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-value">{r['word_count']:,}</div>
                <div class="stat-label">Words</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{r['pair_count']:,}</div>
                <div class="stat-label">Sentences</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{os.path.getsize(r['pdf_path']) / 1024:.0f}</div>
                <div class="stat-label">KB</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if os.path.exists(r["pdf_path"]):
        with open(r["pdf_path"], "rb") as f:
            st.download_button(
                "📥  Download PDF",
                data=f,
                file_name=pdf_name,
                mime="application/pdf",
                use_container_width=True,
            )

# ========== History ==========
history = get_pdf_history()

st.markdown('<div class="history-header">📁  Generated PDFs</div>', unsafe_allow_html=True)

if history:
    for item in history:
        time_str = item["time"].strftime("%m/%d %H:%M")
        st.markdown(f"""
        <div class="history-item">
            <div class="history-icon">📄</div>
            <div class="history-info">
                <div class="history-name">{item['name']}</div>
                <div class="history-meta">{time_str}  ·  {item['size']:.0f} KB</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown('<div class="history-empty">No PDFs yet — paste a link above to get started!</div>', unsafe_allow_html=True)
