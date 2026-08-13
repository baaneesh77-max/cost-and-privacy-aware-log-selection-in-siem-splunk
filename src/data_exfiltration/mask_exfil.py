import re

raw_file = r"D:\Documents\exfil-lab\exfil_http_raw.log"
masked_file = r"D:\Documents\exfil-lab\exfil_http_masked.log"

with open(raw_file, "r", encoding="utf-8") as f:
    data = f.read()

data = re.sub(r"src_ip=\S+", "src_ip=MASKED_IP", data)
data = re.sub(r"user=\S+", "user=MASKED_USER", data)
data = re.sub(r"host=\S+", "host=MASKED_HOST", data)

with open(masked_file, "w", encoding="utf-8") as f:
    f.write(data)