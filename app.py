import os
import re
from flask import Flask, render_template, request, jsonify, send_from_directory
import yt_dlp

app = Flask(__name__)

# ডাউনলোড এবং আপলোড ফোল্ডার কনফিগারেশন
DOWNLOAD_FOLDER = 'downloads'
STATIC_FOLDER = 'static'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')
    platform = data.get('platform', 'youtube')
    
    if not video_url:
        return jsonify({'status': 'error', 'message': 'URL পাওয়া যায়নি!'}), 400

    try:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            basename = os.path.basename(filename)
            
        return jsonify({
            'status': 'success',
            'file_url': f'/get-file/{basename}'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get-file/<filename>')
def get_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

# 🔐 নতুন সিক্রেট অ্যাডমিন ইমেজ আপলোড রুট
@app.route('/admin/upload-profile', methods=['POST'])
def upload_profile():
    password = request.form.get('password')
    if password != '1234':  # আপনার সিক্রেট পাসওয়ার্ড
        return jsonify({'status': 'error', 'message': 'ভুল পাসওয়ার্ড! অ্যাক্সেস ডিনাইড।'}), 403
        
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'কোনো ছবি পাওয়া যায়নি!'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'ফাইলের নাম খালি!'}), 400
        
    # সরাসরি static ফোল্ডারে profile.jpg নামে সেভ হবে (আগেরটা রিপ্লেস হয়ে যাবে)
    file_path = os.path.join(STATIC_FOLDER, 'profile.jpg')
    file.save(file_path)
    
    return jsonify({'status': 'success', 'message': 'প্রোফাইল ছবি সফলভাবে পরিবর্তন হয়েছে!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
