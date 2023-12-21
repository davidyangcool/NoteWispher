from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import whisper
import soundfile as sf
import io
import numpy as np

# 假设您的模型位于此路径
model_path = "./whisper-models/medium.pt"

# 使用Whisper的API加载模型
model = whisper.load_model(model_path)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('record.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(error='No selected file'), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Load Whisper model and transcribe
        # model = whisper.load_model("large")
        result = model.transcribe(filepath)

        # Optionally, remove the uploaded file after transcription if you don't want to keep it
        os.remove(filepath)

        return jsonify(text=result["text"])

    return jsonify(error='Invalid file type'), 400


if __name__ == '__main__':
    app.run(debug=True)
