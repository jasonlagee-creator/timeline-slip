import hashlib
import json
import unittest
from scripts.verify_snapshot import verify

def sample():
    body = "test response"
    obj = {"schema": "timeline-slip-evidence-v1", "comments": [
        {"comment_id": 1, "body": body, "body_sha256": hashlib.sha256(body.encode()).hexdigest()}
    ]}
    raw = json.dumps(obj).encode()
    return raw, hashlib.sha256(raw).hexdigest() + "  snapshot.json"

class VerifySnapshotTests(unittest.TestCase):
    def test_valid(self):
        raw, sidecar = sample()
        self.assertEqual(verify(raw, sidecar), 1)

    def test_modified_snapshot(self):
        raw, sidecar = sample()
        with self.assertRaises(ValueError):
            verify(raw + b"!", sidecar)

    def test_modified_comment_even_if_sidecar_recomputed(self):
        raw, _ = sample()
        obj = json.loads(raw)
        obj["comments"][0]["body"] = "altered"
        altered = json.dumps(obj).encode()
        with self.assertRaises(ValueError):
            verify(altered, hashlib.sha256(altered).hexdigest())

    def test_duplicate_id(self):
        raw, _ = sample()
        obj = json.loads(raw)
        obj["comments"].append(obj["comments"][0])
        altered = json.dumps(obj).encode()
        with self.assertRaises(ValueError):
            verify(altered, hashlib.sha256(altered).hexdigest())

if __name__ == "__main__":
    unittest.main()
