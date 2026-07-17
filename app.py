import os
import logging
import json
from pathlib import Path

from flask import Flask, render_template, request, jsonify
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


if __name__ == '__main__':
    # Use PORT env var when available (useful for platforms like Heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', '1') == '1')
