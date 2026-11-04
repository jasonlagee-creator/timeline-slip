import hashlib
import pathlib
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
            self.assertIn(expected, output.replace(":", "").replace(" ", "").replace("\n", ""))
            self.assertIn("sha256", output)

if __name__ == "__main__":
    unittest.main()
