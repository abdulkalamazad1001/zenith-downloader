#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python Dependencies
pip install -r requirements.txt

# Create directory for FFmpeg
mkdir -p binary_ffmpeg

# Download FFmpeg (Static Build)
if [ ! -f binary_ffmpeg/ffmpeg ]; then
    echo "Downloading FFmpeg..."
    wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
    tar xvf ffmpeg-release-amd64-static.tar.xz -C binary_ffmpeg --strip-components 1
    rm ffmpeg-release-amd64-static.tar.xz
fi

# Download Node.js (for yt-dlp JS execution)
if [ ! -f binary_ffmpeg/node ]; then
    echo "Downloading Node.js..."
    wget https://nodejs.org/dist/v20.10.0/node-v20.10.0-linux-x64.tar.xz
    # Extract to current directory first
    tar xf node-v20.10.0-linux-x64.tar.xz
    # Move the node binary to our target folder
    mv node-v20.10.0-linux-x64/bin/node binary_ffmpeg/
    # Cleanup
    rm -rf node-v20.10.0-linux-x64 node-v20.10.0-linux-x64.tar.xz
fi

# Make executable
chmod +x binary_ffmpeg/ffmpeg
chmod +x binary_ffmpeg/ffprobe
chmod +x binary_ffmpeg/node

echo "FFmpeg installed to $(pwd)/binary_ffmpeg"
