from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    ydl_opts = {'format': 'best', 'outtmpl': 'downloads/%(title)s.%(ext)s'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'message': 'ডাউনলোড সফল হয়েছে!'})
    except Exception as e:
        return jsonify({'message': f'এরর: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
