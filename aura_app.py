from flask import Flask, request, jsonify
from flask import send_file
import subprocess
import os
#venv\Scripts\python "C:\Users\Sahi\OneDrive\Desktop\convert_audio_comm\aura_app.py"
app = Flask(__name__)

@app.route('/embed', methods=['POST'])
def embed():
    try:
        message = request.form['message']
        audio = request.files['audio']
        image = request.files['image']

        # Save uploaded files
        audio.save("audio/input.wav")
        image.save("image/context.jpg")

        # Save message to a temp file so sender2.py can read it
        with open("message.txt", "w") as f:
            f.write(message)

        # Run sender
        result = subprocess.run(["python", "sender2.py"], capture_output=True, text=True)

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

        # Save uploaded files
        audio.save("audio/stego.wav")
        image.save("image/context.jpg")

        # Run receiver
        result = subprocess.run(["python", "receiver2.py"], capture_output=True, text=True)

        return jsonify({"status": "ok", "output": result.stdout})

    except Exception as e:
        return jsonify({"status": "error", "output": str(e)})


if __name__ == "__main__":
    app.run(debug=True)