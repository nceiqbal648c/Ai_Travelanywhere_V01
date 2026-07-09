import os
import shutil
import re
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
    dl_type = data.get('type', 'video')
    
    if not url:
        return jsonify({"message": "লিঙ্ক দেওয়া হয়নি!"}), 400

    # ফাইল নেম খুব বড় হওয়া আটকাতে টাইটেল ছোট করার রুল
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title).50s.%(ext)s'),
    }

    if dl_type == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'best',
            'merge_output_format': 'mp4'
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # অডিওর ক্ষেত্রে এক্সটেনশন mp3 তে পরিবর্তন করা
            if dl_type == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'

        # ফোনের মেইন ডাউনলোড ফোল্ডারে পাঠানো
        phone_download_dir = '/storage/emulated/0/Download/AI_Travel_App'
        
        # ফোল্ডার না থাকলে স্বয়ংক্রিয়ভাবে তৈরি করার লজিক (যা আগে ছিল না)
        if not os.path.exists(phone_download_dir):
            os.makedirs(phone_download_dir, exist_ok=True)

        if os.path.exists(filename):
            destination = os.path.join(phone_download_dir, os.path.basename(filename))
            shutil.copy2(filename, destination)
            return jsonify({"status": "success", "message": "ডাউনলোড সম্পন্ন হয়েছে!"})
        else:
            return jsonify({"status": "error", "message": "ফাইল খুঁজে পাওয়া যায়নি!"}), 404

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
