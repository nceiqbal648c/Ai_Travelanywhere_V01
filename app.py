import os
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, flash
import yt_dlp

app = Flask(__name__)
app.secret_key = 'ai-travel-anywhere-key'

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

ADMIN_PASSWORD = "IqbalTravel2026"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')
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
        return jsonify({'status': 'success', 'file_url': f'/get-file/{basename}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get-file/<filename>')
def get_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

@app.route('/upload-profile', methods=['POST'])
def upload_profile():
    input_password = request.form.get('profile_password')
    file = request.files.get('profile_jpg')
    
    if input_password == ADMIN_PASSWORD:
        if file and file.filename != '':
            upload_path = "/data/data/com.termux/files/home/AI_Travel_App/static/profile.jpg"
            file.save(upload_path)
            print("Image updated successfully!")
            flash("সফলভাবে প্রোফাইল ছবি আপডেট হয়েছে!")
        else:
            flash("ছবি সিলেক্ট করেননি!")
    else:
        print("Unauthorized attempt: Wrong password!")
        flash("ভুল পাসওয়ার্ড! অ্যাক্সেস নেই।")
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
