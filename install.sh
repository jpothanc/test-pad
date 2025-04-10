#!/bin/bash

# === Configuration ===
ART_URL="http://www.art/nodejs"
PACKAGE_NAME="nodejs-18.19.1-1.x86_64.rpm"  # Change to your actual package name
DOWNLOAD_DIR="/tmp"

# === Download the package ===
echo "Downloading Node.js package from Nexus..."
curl -o "$DOWNLOAD_DIR/$PACKAGE_NAME" "$ART_URL/$PACKAGE_NAME"

# === Check if download was successful ===
if [[ ! -f "$DOWNLOAD_DIR/$PACKAGE_NAME" ]]; then
    echo "Download failed: $PACKAGE_NAME not found."
    exit 1
fi

# === Install the package ===
echo "Installing Node.js..."
sudo yum install -y "$DOWNLOAD_DIR/$PACKAGE_NAME"

# === Check installation ===
if command -v node >/dev/null 2>&1; then
    echo "Node.js installed successfully. Version: $(node -v)"
else
    echo "Node.js installation failed."
    exit 2
fi
