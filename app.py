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
    platform = data.get('platform', 'youtube') # ফ্রন্টএন্ড থেকে প্ল্যাটফর্ম রিসিভ করা
    dl_type = data.get('type', 'video')
    
    if not url:
        return jsonify({"status": "error", "message": "লিঙ্ক দেওয়া হয়নি!"}), 400

    # ফেসবুক বা টিকটকের টাইটেল অনেক সময় অদ্ভুত হয়, তাই সেফগার্ড হিসেবে জেনেশুনে ছোট করা
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{platform}_%(title).30s.%(ext)s'),
        'ignoreerrors': True,
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
        # ফেসবুক ও টিকটকের জন্য বেস্ট কোয়ালিটি MP4 নিশ্চিত করা
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                # যদি এক্সট্রাক্ট করতে না পারে, তবে প্রথম এন্ট্রি চেক করা (প্লেলিস্ট বা রিলসের জন্য)
                if 'entries' in info and info['entries']:
                    info = info['entries'][0]
                else:
                    return jsonify({"status": "error", "message": "ভিডিও প্রসেস করা যায়নি! লিঙ্কটি আবার চেক করুন।"}), 400
            
            filename = ydl.prepare_filename(info)
            
            if dl_type == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'

        phone_download_dir = '/storage/emulated/0/Download/AI_Travel_App'
        os.makedirs(phone_download_dir, exist_ok=True)

        # যদি yt_dlp কোনো কারণে ফাইল খুঁজে না পায়, তবে ডিরেক্টরির ফাইল চেক করা
        if not os.path.exists(filename):
            # এক্সটেনশন ছাড়া ম্যাচিং চেক
            base_name = os.path.splitext(filename)[0]
            files = os.listdir(DOWNLOAD_FOLDER)
            for f in files:
                if f.startswith(os.path.basename(base_name)):
                    filename = os.path.join(DOWNLOAD_FOLDER, f)
                    break

        if os.path.exists(filename):
            destination = os.path.join(phone_download_dir, os.path.basename(filename))
            shutil.copy2(filename, destination)
            return jsonify({"status": "success", "message": "ডাউনলোড সম্পন্ন হয়েছে!"})
        else:
            return jsonify({"status": "error", "message": "ফাইলটি ফোনে সেভ করা যায়নি!"}), 404

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
