from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    url = request.json.get('url')
    # কোনো ফরম্যাট বা কুকি ছাড়াই সরাসরি এক্সট্রাক্ট করার চেষ্টা
    ydl_opts = {
        'noplaylist': True,
        'quiet': False, # এরর দেখার জন্য এটা False করলাম
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            # সরাসরি ইনফো ডিকশনারি থেকে url বের করা
            video_url = info.get('url') or info.get('manifest_url')
            return jsonify({'download_url': video_url})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
