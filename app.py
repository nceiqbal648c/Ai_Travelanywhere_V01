import os
import shutil
from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json() or {}
    url = data.get('url')
    platform = data.get('platform', 'youtube')
    
    if not url:
        return jsonify({"status": "error", "message": "লিঙ্ক দেওয়া হয়নি!"}), 400

    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{platform}_%(title).30s.%(ext)s'),
        'ignoreerrors': True,
    }

    # প্রতিটি বাটন অনুযায়ী সঠিক ভিডিও ফরম্যাট ফোর্স করা
    if platform == 'facebook':
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    elif platform == 'tiktok':
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
    else:
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                return jsonify({"status": "error", "message": "লিঙ্ক থেকে ভিডিও প্রসেস করা যায়নি!"}), 400
            filename = ydl.prepare_filename(info)

        phone_download_dir = '/storage/emulated/0/Download/AI_Travel_App'
        os.makedirs(phone_download_dir, exist_ok=True)

        if not os.path.exists(filename):
            base_name = os.path.splitext(filename)[0]
            for f in os.listdir(DOWNLOAD_FOLDER):
                if f.startswith(os.path.basename(base_name)):
                    filename = os.path.join(DOWNLOAD_FOLDER, f)
                    break

        if os.path.exists(filename):
            destination = os.path.join(phone_download_dir, os.path.basename(filename))
            shutil.copy2(filename, destination)
            return jsonify({"status": "success", "platform": platform})
        else:
            return jsonify({"status": "error", "message": "ফাইল ফোনে পাঠানো যায়নি।"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
