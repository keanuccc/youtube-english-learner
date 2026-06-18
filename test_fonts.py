import platform
import os

def test_font_detection():
    """Test font detection on current system."""
    system = platform.system()
    print(f"Operating System: {system}")
    print()

    if system == "Windows":
        font_dir = "C:/Windows/fonts"
        print(f"Windows font directory: {font_dir}")

        simhei = os.path.join(font_dir, "simhei.ttf")
        simsun = os.path.join(font_dir, "simsun.ttc")

        print(f"simhei.ttf exists: {os.path.exists(simhei)}")
        print(f"simsun.ttc exists: {os.path.exists(simsun)}")

        if os.path.exists(simhei):
            print(f"[SUCCESS] Chinese fonts available!")
            return True

    elif system == "Linux":
        print("Checking Linux font directories...")

        linux_font_dirs = [
            "/usr/share/fonts/truetype/wqy",
            "/usr/share/fonts/truetype/noto",
            "/usr/share/fonts/opentype/noto",
            "/usr/share/fonts/truetype/dejavu",
            "/usr/share/fonts",
        ]

        for font_dir in linux_font_dirs:
            if os.path.exists(font_dir):
                print(f"\nChecking: {font_dir}")

                # Walk through subdirectories
                for root, dirs, files in os.walk(font_dir):
                    for font_file in files:
                        font_lower = font_file.lower()
                        if "wqy" in font_lower or "microhei" in font_lower:
                            path = os.path.join(root, font_file)
                            print(f"[SUCCESS] Found Chinese font: {path}")
                            return True

        # If no Chinese font found
        print("\n[WARNING] No Chinese fonts found!")
        print("\nAvailable fonts:")
        for font_dir in linux_font_dirs:
            if os.path.exists(font_dir):
                for root, dirs, files in os.walk(font_dir):
                    for font_file in files[:5]:  # Show first 5
                        print(f"  - {os.path.join(root, font_file)}")

    print("\n[FAILED] Chinese fonts not available")
    return False

if __name__ == "__main__":
    success = test_font_detection()
    if success:
        print("\n✓ System is ready for PDF generation with Chinese text")
    else:
        print("\n✗ System needs Chinese fonts installed")