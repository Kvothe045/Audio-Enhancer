from flask import Flask, render_template, request, send_file
import os
from audio_enhancer import enhance_audio_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ENHANCED_FOLDER = 'enhanced'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENHANCED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        enhanced_file_path = enhance_audio_file(file_path)
        return send_file(enhanced_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
