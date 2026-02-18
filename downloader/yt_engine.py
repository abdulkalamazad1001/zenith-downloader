import yt_dlp
import os
from utils.system_check import check_ffmpeg

# Add local binary folder to PATH so yt-dlp can find 'ffmpeg' and 'node'
# This is crucial for Render deployment where we install them locally
local_bin = os.path.join(os.getcwd(), 'binary_ffmpeg')
if os.path.exists(local_bin):
    os.environ["PATH"] += os.pathsep + local_bin

def get_video_info(url):
    """
    Fetches video information and available formats.
    Returns: dict with title, thumbnail, and list of formats.
    """
    has_ffmpeg = check_ffmpeg()
    
    options = {
        "quiet": True,
        "noplaylist": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"],
            }
        }
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formats = []
            seen_res = set()
            
            # Helper to normalize resolution
            def normalize_res(h):
                # Standard Landscape Heights
                standards = [144, 240, 360, 480, 720, 1080, 1440, 2160, 4320]
                
                # Vertical Heights Map (Height -> Label)
                vertical_map = {
                    1920: 1080,
                    1280: 720,
                    960: 540,
                    640: 360
                }
                
                # Check exact generic match first
                if h in vertical_map:
                    return f"{vertical_map[h]}p"
                
                # Find closest standard
                closest = min(standards, key=lambda x: abs(x - h))
                if abs(closest - h) < (closest * 0.1):
                    return f"{closest}p"
                
                # Check closest vertical
                closest_v = min(vertical_map.keys(), key=lambda x: abs(x - h))
                if abs(closest_v - h) < (closest_v * 0.1):
                     return f"{vertical_map[closest_v]}p"

                return f"{h}p"

            # Simple format filtering
            for f in info.get('formats', []):
                # We only want video formats (or mixed) that have a resolution
                res = f.get('height')
                ext = f.get('ext')
                fid = f.get('format_id')
                vcodec = f.get('vcodec', 'none')
                acodec = f.get('acodec', 'none')
                
                # Filter Logic:
                # 1. Must have resolution (be a video)
                # 2. Must be mp4 or webm (common formats)
                if not res or ext not in ['mp4', 'webm']:
                    continue

                # 3. Critical: If no FFmpeg, only allow files that ALREADY have both Audio and Video.
                #    Downloading video-only (vcodec!=none, acodec==none) requires merging, which will fail.
                if not has_ffmpeg:
                    if vcodec == 'none' or acodec == 'none':
                        continue
                
                # Create a readable label
                # Add a marker if it's video-only (though with the above logic, we might filter them out if no ffmpeg)
                res_label = normalize_res(res)
                label = f"{res_label} ({ext})"
                
                # Check for uniqueness
                if label not in seen_res:
                    formats.append({'id': fid, 'label': label, 'res': res, 'ext': ext})
                    seen_res.add(label)
            
            # Sort by resolution descending
            formats.sort(key=lambda x: x['res'], reverse=True)
            
            # Thumbnail Fallback
            thumb = info.get('thumbnail')
            if not thumb and info.get('thumbnails'):
                # Get the last one (usually highest quality)
                thumb = info.get('thumbnails')[-1].get('url')

            return {
                "title": info.get('title'),
                "thumbnail": thumb,
                "formats": formats
            }
        except Exception as e:
            print(f"Error fetching info: {e}")
            return None

def build_options(platform, format_id=None, progress_hook=None):
    """
    Configures yt-dlp options.
    If format_id is provided, downloads that specific format.
    If format_id is 'audio', downloads best audio and converts to mp3.
    Otherwise adapts to availability of ffmpeg.
    """
    
    options = {
        "quiet": True,
        "noplaylist": True,
        "outtmpl": "downloads/%(extractor)s/%(title)s.%(ext)s",
        "restrictfilenames": True, # Avoid special characters causing filesystem issues
    }

    # Add Android Client to bypass 429/Sign-in errors
    options['extractor_args'] = {
        'youtube': {
            'player_client': ['android', 'web'],
        }
    }

    if format_id == 'audio':
        # Audio extraction mode
        options.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif format_id:
        # User selected a specific video format
        if has_ffmpeg:
             # Try to merge best audio with the selected video if it's video-only
             options['format'] = f"{format_id}+bestaudio/best"
             options['merge_output_format'] = "mp4"
             # Force AAC audio for compatibility (Fixes Opus on Windows)
             options['postprocessor_args'] = {'merger': ['-c:a', 'aac']}
        else:
             # Direct download of the selected format
             options['format'] = format_id
    else:
        # Default behavior (Best available)
        if has_ffmpeg:
            options['format'] = "bestvideo+bestaudio/best"
            options['merge_output_format'] = "mp4"
        else:
            options['format'] = "best"

    return options

def run_downloader(url, options):
    print(f"DEBUG: Starting download for {url} with options: {options}")
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        print(f"DEBUG: Initial filename from prepare_filename: {filename}")
        
        # Check for MP3 audio conversion
        if options.get('postprocessors'):
            for pp in options['postprocessors']:
                if pp.get('key') == 'FFmpegExtractAudio' and pp.get('preferredcodec') == 'mp3':
                    base, _ = os.path.splitext(filename)
                    mp3_file = f"{base}.mp3"
                    print(f"DEBUG: Checking for MP3: {mp3_file}")
                    return mp3_file

        # Check for Video Merge (mp4)
        if options.get('merge_output_format') == 'mp4':
             base, _ = os.path.splitext(filename)
             potential_filename = f"{base}.mp4"
             print(f"DEBUG: Checking for Merged MP4: {potential_filename}")
             if os.path.exists(potential_filename):
                 print("DEBUG: Found Merged MP4")
                 return potential_filename
        
        if os.path.exists(filename):
            print(f"DEBUG: Found original filename: {filename}")
            return filename
            
        print(f"DEBUG: File not found. Returning expected: {filename}")
        return filename
