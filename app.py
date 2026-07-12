from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os
import time

app = Flask(__name__)
OUTPUT_FILE = "/sdcard/Download/downloaded_video.mp4"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"status": "error", "message": "URL missing"}), 400
    
    # পুরোনো ফাইল ডিলিট করা
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    
    try:
        # সুপার ফাস্ট ডাউনলোড (কোনো পার্ট ফাইল ছাড়া)
        subprocess.run(['yt-dlp', '--no-part', '-f', 'best[ext=mp4]', '--no-check-certificate', '-o', OUTPUT_FILE, url], check=True)
        
        # ফাইলটি পুরোপুরি রাইট হওয়ার জন্য ১ সেকেন্ড অপেক্ষা করবে
        time.sleep(1)
        
        if os.path.exists(OUTPUT_FILE):
            return send_file(OUTPUT_FILE, as_attachment=True)
        else:
            return jsonify({"status": "error", "message": "Download failed"}), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
