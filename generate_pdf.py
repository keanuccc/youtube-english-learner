"""Generate bilingual PDF for English learning (practice-book style)."""

import os
from datetime import datetime
from fpdf import FPDF

# Windows Chinese fonts
FONT_DIR = "C:/Windows/fonts"


class BilingualPDF(FPDF):
    """PDF with bilingual content, large spacing for note-taking."""

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.add_font("simhei", "", os.path.join(FONT_DIR, "simhei.ttf"))
        self.add_font("simsun", "", os.path.join(FONT_DIR, "simsun.ttc"))
        self.set_auto_page_break(auto=True, margin=25)

    def footer(self):
        self.set_y(-15)
        self.set_font("simsun", "", 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"- {self.page_no()} -", align="C")


def generate_pdf(pairs, title, channel, output_dir="output"):
    """
    Generate a bilingual PDF from English-Chinese pairs.

    Args:
        pairs: list of (english, chinese) tuples
        title: video title
        channel: channel name
        output_dir: where to save the PDF
    Returns:
        path to the generated PDF
    """
    os.makedirs(output_dir, exist_ok=True)

    safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in title)[:50].strip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_name}_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)

    pdf = BilingualPDF()
    pdf.add_page()

    # === Title page ===
    pdf.set_font("simhei", "", 24)
    pdf.set_text_color(30, 30, 30)
    pdf.ln(40)
    pdf.multi_cell(0, 12, title, align="C")

    pdf.ln(8)
    pdf.set_font("simsun", "", 13)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, channel, align="C")

    pdf.ln(12)
    pdf.set_font("simsun", "", 10)
    pdf.cell(0, 8, datetime.now().strftime("%Y/%m/%d"), align="C")

    pdf.ln(15)
    pdf.set_font("simsun", "", 10)
    pdf.set_text_color(130, 130, 130)
    pdf.cell(0, 8, f"Total: {len(pairs)} sentences", align="C")

    # === Content ===
    margin = 20
    content_w = 210 - margin * 2

    for en, cn in pairs:
        # New page if less than 50mm remaining
        if pdf.get_y() > 297 - 50:
            pdf.add_page()

        # Separator line
        pdf.set_draw_color(200, 200, 200)
        y = pdf.get_y()
        pdf.line(margin, y, 210 - margin, y)
        pdf.ln(4)

        # English text - 14pt bold
        pdf.set_font("simsun", "", 14)
        pdf.set_text_color(30, 30, 30)
        pdf.set_x(margin)
        pdf.multi_cell(content_w, 7, en)

        # Blank space for note-taking (~10mm)
        pdf.ln(5)

        # Chinese translation - 11pt gray
        pdf.set_font("simsun", "", 11)
        pdf.set_text_color(100, 100, 100)
        pdf.set_x(margin)
        pdf.multi_cell(content_w, 6, cn)

        # Trailing space before next pair
        pdf.ln(8)

    pdf.output(filepath)
    return filepath
