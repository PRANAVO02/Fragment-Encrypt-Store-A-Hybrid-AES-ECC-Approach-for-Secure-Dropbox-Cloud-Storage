import os
import shutil
import dropbox
from flask import Flask, render_template, request, redirect, send_file, flash, url_for
from werkzeug.utils import secure_filename

from utils.metadata import load_registry
from encrypt_and_upload import encrypt_and_upload
from download_and_decrypt import decrypt_and_reconstruct
from config import *

# Flask setup
app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for flash messages

dbx = dropbox.Dropbox(ACCESS_TOKEN)


@app.route("/")
def index():
    """Home page with file list"""
    registry = load_registry()
    return render_template("index.html", files=list(registry.keys()))


@app.route("/upload", methods=["POST"])
def upload_file():
    """Upload + encrypt + push to Dropbox"""
    if "file" not in request.files:
        flash("No file part")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    filepath = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    try:
        encrypt_and_upload(filepath)
        flash(f"✅ File '{filename}' uploaded successfully with hybrid encryption.")
    except Exception as e:
        flash(f"❌ Upload failed: {str(e)}")

    return redirect(url_for("index"))


@app.route("/download/<filename>")
def download_file(filename):
    """Download + decrypt + reconstruct"""
    try:
        reconstructed_path = decrypt_and_reconstruct(filename)
        return send_file(reconstructed_path, as_attachment=True)
    except Exception as e:
        flash(f"❌ Download failed: {str(e)}")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
