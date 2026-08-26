from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import wave
import numpy as np
import matplotlib.pyplot as plt
app = Flask(__name__, template_folder="templates")
CORS(app)

print("RUNNING CORRECT SERVER.PY")

# -------------------- PAGES --------------------
@app.route('/')
def home():
    return render_template("index1.html")

@app.route('/sender')
def sender_page():
    return render_template("sender.html")

@app.route('/receiver')
def receiver_page():
    return render_template("receiver.html")


# -------------------- EMBED --------------------

@app.route('/embed', methods=['POST'])
def embed():
    try:
        message = request.form['message']
        audio = request.files['audio']
        image = request.files['image']

        # Save uploaded files
        audio.save("audio/input.wav")
        image.save("image/context.jpg")

        # Save message to file
        with open("message.txt", "w") as f:
            f.write(message)

        result = subprocess.run(
            ["venv\\Scripts\\python", "sender2.py"],
            capture_output=True,
            text=True)

        print("\n========== SENDER PROCESS LOG ==========")
        print(result.stdout)
        print("========================================\n")

        return jsonify({
        "status": "ok",
        "output": result.stdout})
    

    except Exception as e:
        return jsonify({
            "status": "error",
            "output": str(e)
        })
# -------------------- EXTRACT --------------------
@app.route('/extract', methods=['POST'])
def extract():
    try:
        audio = request.files['audio']
        image = request.files['image']

        # Save uploaded files
        audio.save("audio/stego.wav")
        image.save("image/context.jpg")

        # Run receiver script
        result = subprocess.run(
            ["venv\\Scripts\\python", "receiver2.py"],
            capture_output=True,
            text=True
        )

        output = result.stdout

        # Debug print
        print("Receiver output:")
        print(output)

        # Extract recovered message
        message_line = ""
        for line in output.split("\n"):
            if "Recovered message:" in line:
                message_line = line.split("Recovered message:")[1].strip()

        # If message empty → FAIL
        if message_line == "":
            return jsonify({
                "status": "fail",
                "output": "Decryption failed"
            })
        else:
            return jsonify({
                "status": "ok",
                "output": message_line
            })

    except Exception as e:
        return jsonify({
            "status": "error",
            "output": str(e)
        })


# -------------------- DOWNLOAD --------------------

@app.route('/download')
def download():
    return send_file("audio/stego.wav", as_attachment=True)


# -------------------- RUN --------------------

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)