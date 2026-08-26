from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask import send_file
import subprocess
import os

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/embed', methods=['POST'])
def embed():
    try:
        message = request.form['message']
        audio = request.files['audio']
        image = request.files['image']

        audio.save("audio/input.wav")
        image.save("image/context.jpg")

        with open("message.txt", "w") as f:
            f.write(message)

        result = subprocess.run(
            ["venv\\Scripts\\python", "sender2.py"],
            capture_output=True,
            text=True
        )

        return jsonify({"status": "ok", "output": result.stdout})
    except Exception as e:
        return jsonify({"status": "error", "output": str(e)})
@app.route('/download_stego')
def download_stego():
    return send_file("audio/stego.wav", as_attachment=True)
@app.route('/extract', methods=['POST'])
def extract():
    try:
        audio = request.files['audio']
        image = request.files['image']

        audio.save("audio/stego.wav")
        image.save("image/context.jpg")

        result = subprocess.run(
            ["venv\\Scripts\\python", "receiver2.py"],
            capture_output=True,
            text=True
        )

        return jsonify({"status": "ok", "output": result.stdout})
    except Exception as e:
        return jsonify({"status": "error", "output": str(e)})

app.run(debug=False)