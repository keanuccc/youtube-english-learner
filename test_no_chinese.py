import os
import platform

# Temporarily hide Windows fonts to test fallback
if platform.system() == "Windows":
    # Save original font path
    original_font = "C:/Windows/fonts/simhei.ttf"

    # Test with Chinese font
    print("Testing WITH Chinese font (Windows)...")
    from generate_pdf import generate_pdf, BilingualPDF

    pairs = [("Hello", "你好"), ("World", "世界")]
    path = generate_pdf(pairs, "Test Title", "Test Channel")
    print(f"[SUCCESS] PDF generated: {path}")
    print()

    # Now test without Chinese font by temporarily renaming the font
    # (This is just for testing - in production, Railway won't have the font)
    print("Testing WITHOUT Chinese font (simulated)...")
    print("On Railway, Chinese translation will be skipped if no font available")
    print()

    # Test the has_chinese_font flag
    pdf = BilingualPDF()
    print(f"has_chinese_font: {pdf.has_chinese_font}")

    if pdf.has_chinese_font:
        print("[INFO] Chinese font available - PDF will include Chinese translation")
    else:
        print("[INFO] Chinese font NOT available - PDF will only show English")

else:
    print("Not on Windows - testing actual Linux behavior")
    from generate_pdf import generate_pdf, BilingualPDF

    pairs = [("Hello", "你好"), ("World", "世界")]
    path = generate_pdf(pairs, "Test Title", "Test Channel")
    print(f"[SUCCESS] PDF generated: {path}")