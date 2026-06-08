import os
from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

DOWNLOAD_FOLDER = os.path.expanduser('~/downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('imdex.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url', '').strip()
    download_type = data.get('type', 'video') # video or audio
    
    if not video_url:
        return jsonify({"status": "error", "message": "Link thikmoto din!"}), 400
        
    # বাটন অনুযায়ী ফরম্যাট সিলেকশন লজিক
    if download_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s_audio.%(ext)s'),
            'quiet': True,
        }
    else:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'quiet': True,
        }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'File')
            filename = ydl.prepare_filename(info)
            
            phone_download = "/sdcard/Download"
            if os.path.exists(phone_download):
                os.system(f'cp "{filename}" "{phone_download}/"')
                
        return jsonify({"status": "success", "message": f"'{title}' download hoyeche!"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
