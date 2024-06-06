from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
from audio_enhancer import music_audio_enhancer, podcast_audio_enhancer, movie_and_other_audio_enhancer

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages
UPLOAD_FOLDER = 'uploads'
ENHANCED_FOLDER = 'enhanced'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENHANCED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'mkv', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        enhancement_type = request.form.get('enhancement_type')
        try:
            if enhancement_type == 'music':
                enhanced_file_path = music_audio_enhancer(file_path)
            elif enhancement_type == 'podcast':
                enhanced_file_path = podcast_audio_enhancer(file_path)
            elif enhancement_type == 'movie':
                enhanced_file_path = movie_and_other_audio_enhancer(file_path)
            else:
                flash('Invalid enhancement type selected')
                return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error processing file: {str(e)}")
            return redirect(url_for('index'))

        return send_file(enhanced_file_path, as_attachment=True)
    else:
        flash('Unsupported file format!')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
