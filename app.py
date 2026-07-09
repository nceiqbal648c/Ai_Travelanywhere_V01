import os
from flask import Flask, render_template, request, jsonify, send_from_directory
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

    # ইউনিক ও মেমোরি-সেভিং নাম তৈরি
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{platform}_%(title).20s.%(ext)s'),
        'ignoreerrors': True,
    }

    # অল প্ল্যাটফর্ম অপ্টিমাইজড MP4 ফরম্যাট ফোর্স করা (ইউজারের মেমোরি বাঁচাতে)
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
                return jsonify({"status": "error", "message": "ভিডিও প্রসেস করা যায়নি!"}), 400
            filename = ydl.prepare_filename(info)

        if not os.path.exists(filename):
            base_name = os.path.splitext(filename)[0]
            for f in os.listdir(DOWNLOAD_FOLDER):
                if f.startswith(os.path.basename(base_name)):
                    filename = os.path.join(DOWNLOAD_FOLDER, f)
                    break

        if os.path.exists(filename):
            file_title = os.path.basename(filename)
            return jsonify({
                "status": "success", 
                "platform": platform, 
                "file_url": f"/get-file/{file_title}"
            })
        else:
            return jsonify({"status": "error", "message": "ফাইলটি সার্ভারে পাওয়া যায়নি।"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get-file/<filename>')
def get_file(filename):
    # ডিরেক্ট ফোনে ডাউনলোড প্রম্পট ট্রিগার করার সিকিউরড রুট
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
