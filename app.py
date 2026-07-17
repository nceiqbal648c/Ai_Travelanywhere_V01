  GNU nano 9.1        app.py
from flask import Flask, render_template, req>
import yt_dlp
import json
import subprocess
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024>

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

@app.route('/api/video-info', methods=['POST'>
def get_video_info():
    """Get video information from URL"""
    try:
        video_url = request.json.get('url')

        if not video_url:
            return jsonify({'error': 'URL is >

        logger.info(f"Fetching info for: {vid>

        result = subprocess.run(
            ['yt-dlp', '--dump-single-json', >
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            logger.error(f"yt-dlp error: {res>
            return jsonify({'error': 'Failed >
