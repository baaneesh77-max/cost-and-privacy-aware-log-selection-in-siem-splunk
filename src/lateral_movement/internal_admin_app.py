from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "/shared-logs/lateral_movement_raw.log"

def write_log(event_type, username, client_ip, target_host, action, status):
    ts = datetime.utcnow().isoformat()
    line = f"time={ts} event_type={event_type} username={username} client_ip={client_ip} target_host={target_host} action={action} status={status}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

@app.route("/internal")
def internal():
    username = request.args.get("username", "unknown_user")
    src_ip = request.args.get("src_ip", request.remote_addr)
    write_log("internal_access", username, src_ip, "internal-admin", "admin_resource_access", "success")
    return f"Internal admin area reached by {username}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)