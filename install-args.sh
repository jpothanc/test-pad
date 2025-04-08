#!/bin/bash

# === Usage ===
# ./install_node_yum.sh <full_package_url> <install_flag>
# Example:
# ./install_node_yum.sh http://www.nexus/nodejs/nodejs-18.19.1-1.x86_64.rpm true

# === Input arguments ===
PACKAGE_URL="$1"
INSTALL_FLAG="$2"

# === Validate input ===
if [[ -z "$PACKAGE_URL" ]]; then
  echo "Error: Package URL is required."
  echo "Usage: $0 <full_package_url> <install_flag:true|false>"
  exit 1
fi

FILENAME=$(basename "$PACKAGE_URL")
DOWNLOAD_DIR="/tmp"
PACKAGE_PATH="$DOWNLOAD_DIR/$FILENAME"

# === Download the RPM package ===
echo "Downloading $FILENAME from $PACKAGE_URL..."
curl -fSL -o "$PACKAGE_PATH" "$PACKAGE_URL"

# === Check download ===
if [[ ! -f "$PACKAGE_PATH" ]]; then
  echo "Download failed: $FILENAME not found in $DOWNLOAD_DIR."
  exit 2
fi

echo "Downloaded to $PACKAGE_PATH"

# === Install if flag is true ===
if [[ "$INSTALL_FLAG" == "true" ]]; then
  echo "Installing $FILENAME..."
  sudo yum install -y "$PACKAGE_PATH"

  if command -v node >/dev/null 2>&1; then
    echo "✅ Node.js installed successfully. Version: $(node -v)"
  else
    echo "❌ Node.js installation failed."
    exit 3
  fi
else
  echo "Skipping installation. Package downloaded only."
fi
