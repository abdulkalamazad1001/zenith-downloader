from flask import Flask, render_template, request, jsonify, send_file
from downloader.orchestrator import download_media, get_media_info
from utils.system_check import check_ffmpeg
import os
import sys
import threading
import time

app = Flask(__name__)

# Global dictionary to store progress: {download_id: {'percent': 0, 'status': 'Starting...'}}
download_progress = {}

# Check for FFmpeg at startup
if not check_ffmpeg():
    print("WARNING: 'ffmpeg' not found in system PATH.")
    print("High-quality downloads (1080p+) and merging (Video+Audio) will fail or fallback to lower quality.")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-info', methods=['POST'])
def get_info():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
        
    success, result = get_media_info(url)
    
    if success:
        return jsonify({"success": True, "info": result})
    else:
        return jsonify({"success": False, "error": result}), 400

@app.route('/progress/<download_id>')
def progress(download_id):
    return jsonify(download_progress.get(download_id, {'percent': 0, 'status': 'Not found'}))

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    format_id = data.get('format_id') # Optional
    download_id = data.get('download_id') # Required for progress
    
    if not url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
        
    # Define callback to update global progress dict
    def update_progress(percent, status):
        if download_id:
            download_progress[download_id] = {'percent': percent, 'status': status}

    success, result = download_media(url, format_id, progress_callback=update_progress if download_id else None)
    
    if success:
        # result is the filepath
        try:
            filename = os.path.basename(result)
            return send_file(result, as_attachment=True, download_name=filename)
        except Exception as e:
            return jsonify({"success": False, "error": f"File sending failed: {str(e)}"}), 500
    else:
        # result is the error message
        return jsonify({"success": False, "error": result}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
