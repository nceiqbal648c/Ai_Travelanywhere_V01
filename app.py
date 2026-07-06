from flask import Flask, request, jsonify, send_file, render_template_string
import yt_dlp
import os
import shutil
import traceback

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# আপনার সব বাটন ও ইনপুট বক্সসহ পারফেক্ট ডার্ক UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ai_Travel_Anywhere</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #0b0f19;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            color: white;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .container {
            width: 90%;
            max-width: 450px;
            text-align: center;
            padding: 20px;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 25px;
            font-weight: 600;
        }
        .link-input {
            width: 100%;
            padding: 14px 20px;
            font-size: 15px;
            background-color: #111827;
            border: 1px solid #374151;
            border-radius: 50px;
            color: white;
            box-sizing: border-box;
            outline: none;
            margin-bottom: 20px;
        }
        .link-input:focus {
            border-color: #3b82f6;
        }
        .button-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 12px;
        }
        .btn {
            background-color: #1f2937;
            color: white;
            border: 1px solid #374151;
            padding: 14px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            box-sizing: border-box;
            transition: all 0.2s ease;
        }
        .btn:hover {
            background-color: #374151;
        }
        .btn-main {
            background-color: transparent;
            margin-bottom: 15px;
        }
        .btn-tiktok {
            background-color: #111827;
            margin-top: 12px;
        }
        #status {
            margin-top: 15px;
            font-size: 14px;
            color: #3b82f6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Ai_Travel_Anywhere</h1>
        
        <!-- লিংক পেস্ট করার ইনপুট ফিল্ড -->
        <input type="url" id="urlInput" class="link-input" placeholder="Paste your link here..." required>

        <!-- মেইন ডাউনলোড বাটন -->
        <button onclick="startDownload('video')" class="btn btn-main">DOWNLOAD MEDIA</button>

        <!-- ক্যাটাগরি বাটন গ্রিড -->
        <div class="button-grid">
            <button onclick="startDownload('video')" class="btn">MP4 VIDEO</button>
            <button onclick="startDownload('audio')" class="btn">MP3 AUDIO</button>
            <button onclick="startDownload('video')" class="btn">YOUTUBE</button>
            <button onclick="startDownload('video')" class="btn">FACEBOOK</button>
        </div>
        
        <!-- টিকটক বাটন -->
        <button onclick="startDownload('video')" class="btn btn-tiktok">TIKTOK</button>

        <!-- স্ট্যাটাস দেখানোর জায়গা -->
        <div id="status"></div>
    </div>

    <script>
        function startDownload(type) {
            const url = document.getElementById('urlInput').value;
            const statusDiv = document.getElementById('status');
            
            if (!url) {
                alert('অনুগ্রহ করে আগে লিংক পেস্ট করুন!');
                return;
            }

            statusDiv.innerText = "ডাউনলোড শুরু হয়েছে, দয়া করে অপেক্ষা করুন...";

            // আপনার ব্যাকএন্ডের /download রুটে ডেটা পাঠানো হচ্ছে
            fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url, type: type })
            })
            .then(response => {
                if (response.ok) {
                    statusDiv.innerText = "ডাউনলোড সফল হয়েছে এবং ফোনে সেভ হয়েছে!";
                    return response.blob();
                } else {
                    return response.json().then(err => { throw new Error(err.message); });
                }
            })
            .then(blob => {
                // ব্রাউজারে ফাইল ডাউনলোডের ট্রিগার
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = ""; 
                document.body.appendChild(a);
                a.click();
                a.remove();
            })
            .catch(error => {
                statusDiv.innerText = "এরর: " + error.message;
                alert("ডাউনলোড ব্যর্থ হয়েছে: " + error.message);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json() or {}
    url = data.get('url')
    dl_type = data.get('type', 'video')
    
    if not url:
        return jsonify({"message": "লিংক দেওয়া হয়নি!"}), 400
        
    try:
        if dl_type == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
            }
            
        print("URL =", url)
        print("TYPE =", dl_type)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if dl_type == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'
            elif not filename.endswith('.mp4'):
                filename = os.path.splitext(filename)[0] + '.mp4'
                
        print("FILE=", filename)
        print("EXISTS=", os.path.exists(filename))
        
        # আপনার ফোনের নির্দিষ্ট স্টোরেজ ফোল্ডারে কপি করা
        phone_folder = "/storage/emulated/0/Download/AI_Travel_App"
        os.makedirs(phone_folder, exist_ok=True)
        shutil.copy2(filename, os.path.join(phone_folder, os.path.basename(filename)))
        
        return send_file(filename, as_attachment=True)
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
