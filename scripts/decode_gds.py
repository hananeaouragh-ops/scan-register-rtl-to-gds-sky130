from pathlib import Path
import base64, hashlib
root = Path(__file__).resolve().parents[1] / "results"
data = base64.b64decode((root / "scan_register.gds.b64").read_bytes())
expected = (root / "SHA256SUMS").read_text().split()[0]
assert hashlib.sha256(data).hexdigest() == expected, "GDS checksum mismatch"
p = root / "scan_register.gds"
p.write_bytes(data)
print(p)
