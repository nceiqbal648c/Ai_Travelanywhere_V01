# Ai_Travelanywhere_V01

This repository contains a small Flask app that uses yt-dlp to fetch video metadata and optionally download media.

Quick start (Termux / Linux / macOS):

1. Clone and enter the repo

   git clone https://github.com/nceiqbal648c/Ai_Travelanywhere_V01.git
   cd Ai_Travelanywhere_V01

2. Create and activate a virtual environment

   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies

   pip install --upgrade pip
   pip install -r requirements.txt

4. Run the app

   python app.py

API endpoints

- POST /api/video-info
  - JSON body: {"url": "<video-url>"}
  - Returns video metadata as JSON.

- POST /api/download
  - JSON body: {"url": "<video-url>", "format": "bestaudio", "filename": "optional-name-without-ext"}
  - Downloads file into downloads/ and returns the saved filename.

Notes

- Ensure ffmpeg is installed if you plan to extract or convert audio/video formats.
- The app writes to a local downloads/ directory; make sure the process has write permissions.
