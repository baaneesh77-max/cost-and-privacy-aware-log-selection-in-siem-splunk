from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "/shared-logs/lateral_movement_raw.log"
INTERNAL_URL = "http://internal-admin:5001/internal"

def write_log(event_type, username, client_ip, target_host, action, status):
    ts = datetime.utcnow().isoformat()
    line = f"time={ts} event_type={event_type} username={username} client_ip={client_ip} target_host={target_host} action={action} status={status}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

@app.route("/")
def home():
    return """
    <h2>Public SME Portal</h2>
    <p>Use /login?username=testuser to simulate a user action.</p>
    <p>Use /pivot?username=testuser to simulate lateral movement toward the internal service.</p>
    """

@app.route("/login")
def login():
    username = request.args.get("username", "unknown_user")
    client_ip = request.remote_addr
    write_log("public_access", username, client_ip, "public-web", "login_attempt", "success")
    return f"Public login recorded for {username}"

@app.route("/pivot")
def pivot():
    username = request.args.get("username", "unknown_user")
    client_ip = request.remote_addr
    write_log("lateral_movement", username, client_ip, "internal-admin", "pivot_attempt", "initiated")
    try:
        r = requests.get(f"{INTERNAL_URL}?username={username}&src_ip={client_ip}", timeout=5)
        write_log("lateral_movement", username, client_ip, "internal-admin", "pivot_attempt", "success")
        return f"Pivot attempt response: {r.text}"
    except Exception:
        write_log("lateral_movement", username, client_ip, "internal-admin", "pivot_attempt", "failed")
        return "Pivot failed", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)