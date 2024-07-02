from flask import Flask, request, send_file, render_template, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kontak')
def kontak():
    return render_template('kontak.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict)
        mp3_file = file_name.rsplit('.', 1)[0] + '.mp3'
    
    return jsonify({
        'title': info_dict.get('title', 'No title'),
        'thumbnail': info_dict.get('thumbnail', ''),
        'mp3_file': mp3_file
    })

@app.route('/downloads/<filename>')
def serve_file(filename):
    return send_file(os.path.join('downloads', filename), as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
