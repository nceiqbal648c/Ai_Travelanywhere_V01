import os
import logging
import json
from pathlib import Path

from flask import Flask, render_template, request, jsonify, send_file, abort
import yt_dlp
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__)
# Allow uploads up to 500 MB (adjust as needed)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create directories
Path('downloads').mkdir(exist_ok=True)
Path('logs').mkdir(exist_ok=True)


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/video-info', methods=['POST'])
def get_video_info():
    """Get video information from URL using yt_dlp (no download)."""
    try:
        data = request.get_json(silent=True) or {}
        video_url = data.get('url')

        if not video_url:
            return jsonify({'error': 'URL is required in JSON body under "url" key.'}), 400

        logger.info("Fetching info for: %s", video_url)

        ydl_opts = {
            'quiet': True,
            'nocheckcertificate': True,
            'skip_download': True,
            # don't write metadata to disk
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # extract_info returns a dict-like object with video metadata
            info = ydl.extract_info(video_url, download=False)

        # Some fields may not be JSON-serializable; ensure we return JSON-safe data
        try:
            return jsonify(info)
        except TypeError:
            # Fallback: serialize with json.dumps using default=str
            safe = json.loads(json.dumps(info, default=str))
            return jsonify(safe)

    except yt_dlp.utils.DownloadError as e:
        logger.exception("yt-dlp download error")
        return jsonify({'error': 'yt-dlp failed to fetch info', 'detail': str(e)}), 422
    except Exception as e:
        logger.exception("Unexpected error while fetching video info")
        return jsonify({'error': 'Unexpected error', 'detail': str(e)}), 500


@app.route('/api/download', methods=['POST'])
def download_video():
    """Download a video/audio using yt_dlp into the downloads/ directory.

    JSON body parameters:
      - url: required, the video URL
      - format: optional, yt-dlp format selector (e.g. "bestaudio" or "bestvideo+bestaudio")
      - filename: optional, desired output filename (without path); if omitted yt-dlp will use its template
    Returns JSON with filename on success.
    """
    try:
        data = request.get_json(silent=True) or {}
        video_url = data.get('url')
        fmt = data.get('format')
        user_filename = data.get('filename')  # optional

        if not video_url:
            return jsonify({'error': 'URL is required in JSON body under "url" key.'}), 400

        # Build outtmpl
        if user_filename:
            # ensure no path traversal
            safe_name = os.path.basename(user_filename)
            outtmpl = f"downloads/{safe_name}.%(ext)s"
        else:
            outtmpl = "downloads/%(title)s.%(ext)s"

        ydl_opts = {
            'outtmpl': outtmpl,
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }
        if fmt:
            ydl_opts['format'] = fmt

        logger.info("Starting download for %s with opts %s", video_url, {k: v for k, v in ydl_opts.items() if k != 'outtmpl'})

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            # prepare_filename uses info to construct the final filename
            filename = ydl.prepare_filename(info)

        # Ensure the file exists
        if not os.path.exists(filename):
            logger.warning("yt-dlp reported success but file not found: %s", filename)
            return jsonify({'error': 'download completed but file not found', 'filename': filename}), 500

        # Return relative path
        rel_path = os.path.relpath(filename)
        return jsonify({'status': 'ok', 'filename': rel_path}), 200

    except yt_dlp.utils.DownloadError as e:
        logger.exception("yt-dlp download error")
        return jsonify({'error': 'yt-dlp failed to download', 'detail': str(e)}), 422
    except Exception as e:
        logger.exception("Unexpected error while downloading video")
        return jsonify({'error': 'Unexpected error', 'detail': str(e)}), 500


# compatibility endpoints for older frontend paths
@app.route('/get_info', methods=['POST'])
def get_info_compat():
    """Compatibility wrapper for older frontend using /get_info"""
    return get_video_info()


@app.route('/download', methods=['POST'])
def download_compat():
    """Compatibility wrapper for older frontend using /download"""
    return download_video()


if __name__ == '__main__':
    # Use PORT env var when available (useful for platforms like Heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', '1') == '1')
