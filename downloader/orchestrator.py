from .detector import detect_platform
from .yt_engine import run_downloader, build_options, get_video_info
from utils.validator import validate_url
import os

def get_media_info(url):
    """
    Gets metadata and formats for a URL.
    """
    if not validate_url(url):
        return False, "Invalid URL provided."
    
    platform = detect_platform(url)
    if platform == "unsupported":
        return False, "Platform not supported."
        
    info = get_video_info(url)
    if info:
        return True, info
    else:
        return False, "Could not fetch video info."

def download_media(url, format_id=None, progress_callback=None):
    """
    Main function to handle the download process.
    Returns: (status, message_or_filepath)
    """
    # 1. Validate
    if not validate_url(url):
        return False, "Invalid URL provided."

    # 2. Detect Platform
    platform = detect_platform(url)
    if platform == "unsupported":
        return False, "Platform not supported. Only YouTube, Instagram, and X are supported."

    # 3. Build Options & Download
    try:
        # Define internal hook for yt-dlp
        def internal_hook(d):
            if d['status'] == 'downloading':
                # Calculate percentage
                raw_p = d.get('_percent_str', '0%')
                # Strip ANSI codes if present
                import re
                p = re.sub(r'\x1b\[[0-9;]*m', '', raw_p).replace('%','')
                
                try:
                    percent = float(p)
                except:
                    percent = 0
                
                # print(f"DEBUG: Progress - Raw: {raw_p} -> Parsed: {percent}%") # Uncomment for verbose logs
                
                if progress_callback:
                    progress_callback(percent, "Downloading...")

            elif d['status'] == 'finished':
                if progress_callback:
                    progress_callback(99, "Processing/Converting...")

        options = build_options(platform, format_id, progress_hook=internal_hook)
        filepath = run_downloader(url, options)
        
        if filepath and os.path.exists(filepath):
            if progress_callback:
                 progress_callback(100, "Complete!")
            return True, filepath
        else:
            return False, "Download finished but file not found."
            
    except Exception as e:
        return False, f"Error during download: {str(e)}"
