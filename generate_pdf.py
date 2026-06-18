"""Generate bilingual PDF for English learning (practice-book style)."""

import os
import platform
from datetime import datetime
from fpdf import FPDF


def get_font_paths():
    """Get font paths based on operating system."""
    system = platform.system()

    if system == "Windows":
        # Windows fonts
        font_dir = "C:/Windows/fonts"
        simhei = os.path.join(font_dir, "simhei.ttf")
        simsun = os.path.join(font_dir, "simsun.ttc")
        if os.path.exists(simhei):
            return {"simhei": simhei, "simsun": simsun}

    elif system == "Linux":
        # Try common Linux font locations (after install_fonts.sh runs)
        linux_font_dirs = [
            "/usr/share/fonts/truetype/wqy",
            "/usr/share/fonts/truetype/noto",
            "/usr/share/fonts/opentype/noto",
            "/usr/share/fonts/truetype/dejavu",
            "/usr/share/fonts",
        ]

        # Look for WenQuanYi Micro Hei (most common Chinese font on Linux)
        for font_dir in linux_font_dirs:
            if not os.path.exists(font_dir):
                continue

            # Walk through subdirectories
            for root, dirs, files in os.walk(font_dir):
                for font_file in files:
                    font_lower = font_file.lower()
                    # Look for WenQuanYi Micro Hei specifically
                    if "wqy-microhei" in font_lower or "wqy_microhei" in font_lower:
                        path = os.path.join(root, font_file)
                        print(f"Found Chinese font: {path}")
                        return {"simhei": path, "simsun": path}
                    # Also try WenQuanYi Zen Hei
                    elif "wqy-zenhei" in font_lower or "wqy_zenhei" in font_lower:
                        path = os.path.join(root, font_file)
                        print(f"Found Chinese font: {path}")
                        return {"simhei": path, "simsun": path}
                    # Try Noto Sans CJK
                    elif "noto" in font_lower and "cjk" in font_lower and font_file.endswith(".ttf"):
                        path = os.path.join(root, font_file)
                        print(f"Found Chinese font: {path}")
                        return {"simhei": path, "simsun": path}

        # If no Chinese font found, try to find any TTF font
        for font_dir in linux_font_dirs:
            if not os.path.exists(font_dir):
                continue
            for root, dirs, files in os.walk(font_dir):
                for font_file in files:
                    if font_file.endswith(".ttf"):
                        path = os.path.join(root, font_file)
                        print(f"Using fallback font: {path}")
                        return {"simhei": path, "simsun": path}

    # Last resort: None (will use Helvetica)
    print("No Chinese fonts found on system")
    return {"simhei": None, "simsun": None}


class BilingualPDF(FPDF):
    """PDF with bilingual content, large spacing for note-taking."""

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=25)

        # Load fonts
        font_paths = get_font_paths()
        self.has_chinese_font = False

        # Try to load Chinese fonts
        if font_paths.get("simhei") and os.path.exists(font_paths["simhei"]):
            try:
                self.add_font("simhei", "", font_paths["simhei"])
                self.add_font("simsun", "", font_paths["simsun"])
                self.has_chinese_font = True
                print(f"Loaded Chinese fonts from: {font_paths['simhei']}")
            except Exception as e:
                print(f"Warning: Could not load Chinese fonts: {e}")

        if not self.has_chinese_font:
            print("Warning: Chinese fonts not available, using built-in Helvetica")

    def footer(self):
        self.set_y(-15)
        if self.has_chinese_font:
            self.set_font("simsun", "", 9)
        else:
            self.set_font("Helvetica", "", 9)
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
    print(f"[DEBUG] Generating PDF with {len(pairs)} pairs")
    print(f"[DEBUG] Title: {title}")
    print(f"[DEBUG] Channel: {channel}")

    os.makedirs(output_dir, exist_ok=True)

    safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in title)[:50].strip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_name}_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)

    print(f"[DEBUG] Output path: {filepath}")

    pdf = BilingualPDF()
    pdf.add_page()

    # Select font based on availability
    title_font = "simhei" if pdf.has_chinese_font else "Helvetica"
    body_font = "simsun" if pdf.has_chinese_font else "Helvetica"

    # === Title page ===
    pdf.set_font(title_font, "", 24)
    pdf.set_text_color(30, 30, 30)
    pdf.ln(40)
    pdf.multi_cell(0, 12, title, align="C")

    pdf.ln(8)
    pdf.set_font(body_font, "", 13)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, channel, align="C")

    pdf.ln(12)
    pdf.set_font(body_font, "", 10)
    pdf.cell(0, 8, datetime.now().strftime("%Y/%m/%d"), align="C")

    pdf.ln(15)
    pdf.set_font(body_font, "", 10)
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
        pdf.set_font(body_font, "", 14)
        pdf.set_text_color(30, 30, 30)
        pdf.set_x(margin)
        pdf.multi_cell(content_w, 7, en)

        # Blank space for note-taking (~10mm)
        pdf.ln(5)

        # Chinese translation - 11pt gray
        pdf.set_font(body_font, "", 11)
        pdf.set_text_color(100, 100, 100)
        pdf.set_x(margin)
        pdf.multi_cell(content_w, 6, cn)

        # Trailing space before next pair
        pdf.ln(8)

    pdf.output(filepath)
    return filepath
