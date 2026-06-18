#!/bin/bash
# Install Chinese fonts for PDF generation on Linux/Railway

echo "=========================================="
echo "Installing Chinese fonts for Railway..."
echo "=========================================="

# Check if we're in a container with apt-get
if command -v apt-get &> /dev/null; then
    echo "apt-get found, installing fonts..."

    # Update package list
    echo "Updating package list..."
    apt-get update -qq

    # Install Chinese fonts
    echo "Installing WenQuanYi Micro Hei font..."
    apt-get install -y -qq fonts-wqy-microhei 2>/dev/null || echo "Failed to install fonts-wqy-microhei"

    echo "Installing WenQuanYi Zen Hei font..."
    apt-get install -y -qq fonts-wqy-zenhei 2>/dev/null || echo "Failed to install fonts-wqy-zenhei"

    # Clear font cache
    echo "Updating font cache..."
    fc-cache -fv 2>/dev/null || echo "fc-cache not available"

elif command -v apk &> /dev/null; then
    echo "apk found (Alpine), installing fonts..."
    apk add --no-cache font-wqy-microhei 2>/dev/null || echo "Failed to install font-wqy-microhei"

elif command -v yum &> /dev/null; then
    echo "yum found (RHEL/CentOS), installing fonts..."
    yum install -y wqy-microhei-fonts 2>/dev/null || echo "Failed to install wqy-microhei-fonts"

else
    echo "No package manager found, skipping font installation"
    echo "PDF will use Helvetica (no Chinese support)"
fi

# Verify installation
echo ""
echo "=========================================="
echo "Verifying font installation..."
echo "=========================================="

# Check if fc-list is available
if command -v fc-list &> /dev/null; then
    # Check if fonts are installed
    if fc-list | grep -qi "wqy\|microhei\|zenhei"; then
        echo "[SUCCESS] Chinese fonts installed!"
        echo ""
        echo "Available Chinese fonts:"
        fc-list :lang=zh 2>/dev/null | head -10 || fc-list | grep -i "wqy\|microhei" | head -10
    else
        echo "[WARNING] Chinese fonts not found in font cache"
        echo ""
        echo "All available fonts (first 20):"
        fc-list | head -20
    fi
else
    echo "fc-list not available, cannot verify fonts"
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
    "/usr/share/fonts"
)

for dir in "${FONT_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "Found font directory: $dir"
        ls -la "$dir" 2>/dev/null | head -5
    fi
done

echo ""
echo "Font installation complete!"