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

# Make executable
chmod +x binary_ffmpeg/ffmpeg
chmod +x binary_ffmpeg/ffprobe

echo "FFmpeg installed to $(pwd)/binary_ffmpeg"
