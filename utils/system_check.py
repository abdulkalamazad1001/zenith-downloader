import shutil
import os

def check_ffmpeg():
    """
    Checks if ffmpeg is available in the system PATH.
    Also attempts to add the local tool path if not found.
    Returns: True if found, False otherwise.
    """
    # Try adding the local installation path first
    local_path = r"C:\Users\abdul\.gemini\antigravity\scratch\ffmpeg_tool\ffmpeg-8.0.1-essentials_build\bin"
    if os.path.exists(local_path):
        os.environ["PATH"] += os.pathsep + local_path
        
    return shutil.which("ffmpeg") is not None
