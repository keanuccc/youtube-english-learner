#!/bin/bash
# Install Chinese fonts for PDF generation on Linux/Railway

echo "Installing Chinese fonts..."

# Update package list
apt-get update

# Install Chinese fonts
apt-get install -y fonts-wqy-microhei fonts-wqy-zenhei

# Clear font cache
fc-cache -fv

echo "Chinese fonts installed successfully!"

# Verify installation
echo "Available Chinese fonts:"
fc-list :lang=zh | head -5