@echo off
echo Starting Zenith Downloader...
if not exist "venv" (
    echo Virtual environment not found! Creating one...
    python -m venv venv
    call venv\Scripts\activate
) else (
    call venv\Scripts\activate
)

echo Installing/Updating dependencies...
pip install -r requirements.txt

echo Checking for FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] FFmpeg not found in PATH!
    echo High-quality downloads might fail.
    echo Please install FFmpeg or run 'install_ffmpeg.ps1'
    pause
)

echo Starting Flask Server...
start http://127.0.0.1:5000
python app.py
pause
