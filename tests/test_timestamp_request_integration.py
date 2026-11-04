import hashlib
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest
from scripts.create_timestamp_request import make_request

@unittest.skipUnless(shutil.which("openssl"), "OpenSSL unavailable")
class TimestampRequestIntegrationTests(unittest.TestCase):
    def test_request_contains_snapshot_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = pathlib.Path(tmp) / "snapshot.json"
            request = pathlib.Path(tmp) / "snapshot.tsq"
            snapshot.write_bytes(b'{"schema":"timeline-slip-evidence-v1","comments":[]}')
            expected = hashlib.sha256(snapshot.read_bytes()).hexdigest()
            self.assertEqual(make_request(snapshot, request), expected)
            self.assertGreater(request.stat().st_size, 0)
            output = subprocess.run(
                ["openssl", "ts", "-query", "-in", str(request), "-text"],
                check=True, capture_output=True, text=True
            ).stdout.lower()
            lines = [line for line in output.splitlines() if re.match(r"\s*[0-9a-f]{4} - ", line)]
            hex_bytes = []
            for line in lines:
                hex_column = line.split(" - ", 1)[1].split("   ", 1)[0]
                hex_bytes.extend(re.findall(r"\b[0-9a-f]{2}\b", hex_column.replace("-", " ")))
            self.assertEqual("".join(hex_bytes), expected)
            self.assertIn("sha256", output)

if __name__ == "__main__":
    unittest.main()
