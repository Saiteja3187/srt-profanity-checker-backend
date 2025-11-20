from flask import Flask, request, jsonify
from flask_cors import CORS
from detector import analyze_srt
import os

app = Flask(__name__)

# FIX: Allow all origins (development only)
CORS(app)


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == "OPTIONS":
        return ('', 200)

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if not file.filename.endswith('.srt'):
        return jsonify({"error": "File must be .srt"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    result = analyze_srt(file_path)
    return jsonify(result), 200



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
