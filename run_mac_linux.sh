#!/bin/bash

# Zenith Downloader Startup Script for Mac/Linux

echo "🚀 Starting Zenith Downloader..."

# 1. Check/Install FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg not found!"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "🍎 Please install it using Homebrew: brew install ffmpeg"
    else
        echo "🐧 Please install it using your package manager (e.g., sudo apt install ffmpeg)"
    fi
    exit 1
fi

# 2. Setup Virtual Environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 3. Activate & Install Dependencies
source venv/bin/activate
echo "⬇️ Installing/Updating dependencies..."
pip install -r requirements.txt

# 4. Start Server
echo "✅ Starting Flask Server..."
# Open browser using 'open' (Mac) or 'xdg-open' (Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://127.0.0.1:5000 &
elif command -v xdg-open &> /dev/null; then
    xdg-open http://127.0.0.1:5000 &
fi

python3 app.py
