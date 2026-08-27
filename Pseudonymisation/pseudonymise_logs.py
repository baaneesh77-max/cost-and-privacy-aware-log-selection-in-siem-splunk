import hmac
import hashlib
import base64
import re
from pathlib import Path


KEY_USER = b"user_key"
KEY_IP = b"ip_key"
KEY_SESSION = b"session_key"
KEY_HOST = b"host_key"

# Input/output paths
RAW_DIR = Path(r"D:\Documents\capstone\privacy\raw_logs")
OUT_DIR = Path(r"D:\Documents\capstone\privacy\pseudonymised_logs")

# Ensure output directory exists
OUT_DIR.mkdir(parents=True, exist_ok=True)


def hmac_pseudonym(value: str, key: bytes) -> str:
    """
    Deterministic pseudonym using HMAC-SHA-256 + base64 (URL-safe).
    """
    h = hmac.new(key, value.encode("utf-8"), hashlib.sha256)
    # Use URL-safe base64 and strip padding for compactness
    token = base64.urlsafe_b64encode(h.digest()).rstrip(b"=").decode("ascii")
    return token


def mask_line(line: str) -> str:
    """
    Apply pseudonymisation to:
      - username=...
      - user=...
      - client_ip=...
      - src_ip=...
      - sessionid=...
      - host=...
    """

    # username=...
    def replace_username(m):
        prefix = m.group(1)
        value = m.group(2)
        token = hmac_pseudonym(value, KEY_USER)
        return f"{prefix}{token}"

    line = re.sub(r"(username=)([^\s]+)", replace_username, line, flags=re.IGNORECASE)

    # user=...
    def replace_user(m):
        prefix = m.group(1)
        value = m.group(2)
        token = hmac_pseudonym(value, KEY_USER)
        return f"{prefix}{token}"

    line = re.sub(r"(user=)([^\s]+)", replace_user, line, flags=re.IGNORECASE)

    # client_ip=...
    def replace_client_ip(m):
        prefix = m.group(1)
        value = m.group(2)
        token = hmac_pseudonym(value, KEY_IP)
        return f"{prefix}{token}"

    line = re.sub(r"(client_ip=)([^\s]+)", replace_client_ip, line, flags=re.IGNORECASE)

    # src_ip=...
    def replace_src_ip(m):
        prefix = m.group(1)
        value = m.group(2)
        token = hmac_pseudonym(value, KEY_IP)
        return f"{prefix}{token}"

    line = re.sub(r"(src_ip=)([^\s]+)", replace_src_ip, line, flags=re.IGNORECASE)

    # sessionid=...
    def replace_sessionid(m):
        prefix = m.group(1)
        value = m.group(2)
        token = hmac_pseudonym(value, KEY_SESSION)
        return f"{prefix}{token}"

    line = re.sub(r"(sessionid=)([^\s]+)", replace_sessionid, line, flags=re.IGNORECASE)

    # host=...
    def replace_host(m):
        prefix = m.group(1)
        value = m.group(2)
        token = hmac_pseudonym(value, KEY_HOST)
        return f"{prefix}{token}"

    line = re.sub(r"(host=)([^\s]+)", replace_host, line, flags=re.IGNORECASE)

    return line


def process_file(input_path: Path, output_path: Path):
    with input_path.open("r", encoding="utf-8") as f_in, \
         output_path.open("w", encoding="utf-8") as f_out:
        for line in f_in:
            masked = mask_line(line.rstrip("\n"))
            f_out.write(masked + "\n")


def main():
    # Define mapping: raw filename -> output filename
    files = {
        "sqli_masked_7.log": "sqli_pseudo.log",
        "exfil_masked_4.log": "exfil_pseudo.log",
        "lateral_movement_18.log": "lateral_pseudo.log",
    }

    for raw_name, out_name in files.items():
        in_path = RAW_DIR / raw_name
        out_path = OUT_DIR / out_name
        if not in_path.exists():
            print(f"[SKIP] {in_path} not found")
            continue
        process_file(in_path, out_path)
        print(f"[DONE] {in_path} -> {out_path}")


if __name__ == "__main__":
    main()