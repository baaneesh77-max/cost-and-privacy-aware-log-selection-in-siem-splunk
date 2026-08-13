from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_DIR = r"D:\Documents\exfil-lab\uploads"
LOG_FILE = r"D:\Documents\exfil-lab\exfil_http_raw.log"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file')
    user = request.form.get('user', 'unknown_user')
    host = request.form.get('host', 'unknown_host')
    if not f:
        return "No file", 400

    save_path = os.path.join(UPLOAD_DIR, f.filename)
    f.save(save_path)
    size = os.path.getsize(save_path)

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(
            f"{datetime.now().isoformat()} "
            f"src_ip=127.0.0.1 user={user} host={host} "
            f"filename={f.filename} bytes={size} "
            f"dest_url=http://127.0.0.1:5000/upload method=POST status=200\n"
        )

    return "Uploaded", 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)