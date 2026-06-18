#!/bin/bash
# Install Chinese fonts for PDF generation on Linux/Railway

echo "=========================================="
echo "Installing Chinese fonts for Railway..."
echo "=========================================="

# Update package list
echo "Updating package list..."
apt-get update -qq

# Install Chinese fonts
echo "Installing WenQuanYi Micro Hei font..."
apt-get install -y -qq fonts-wqy-microhei

echo "Installing WenQuanYi Zen Hei font..."
apt-get install -y -qq fonts-wqy-zenhei

# Clear font cache
echo "Updating font cache..."
fc-cache -fv

# Verify installation
echo ""
echo "=========================================="
echo "Verifying font installation..."
echo "=========================================="

# Check if fonts are installed
if fc-list | grep -q "WenQuanYi"; then
    echo "[SUCCESS] Chinese fonts installed!"
    echo ""
    echo "Available Chinese fonts:"
    fc-list :lang=zh | head -10
else
    echo "[WARNING] Fonts may not have installed correctly"
    echo ""
    echo "All available fonts:"
    fc-list | head -20
fi

# Test font file locations
echo ""
echo "=========================================="
echo "Checking font file locations..."
echo "=========================================="

FONT_DIRS=(
    "/usr/share/fonts/truetype/wqy"
    "/usr/share/fonts/opentype/noto"
    "/usr/share/fonts/truetype/noto"
)

for dir in "${FONT_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "Found font directory: $dir"
        ls -la "$dir" | head -5
    fi
done

echo ""
echo "Font installation complete!"