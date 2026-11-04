import json
import unittest
from scripts.prepare_witness import prepare
from scripts.verify_witness import verify_witness

class WitnessConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = b'{"schema":"timeline-slip-evidence-v1","comments":[]}'
        self.request = prepare(self.snapshot)

    def encode(self, obj):
        return json.dumps(obj).encode("utf-8")

    def test_valid_request(self):
        self.assertTrue(verify_witness(self.snapshot, self.encode(self.request)))

    def test_altered_snapshot(self):
        with self.assertRaises(ValueError):
            verify_witness(self.snapshot + b" ", self.encode(self.request))

    def test_altered_digest(self):
        self.request["snapshot_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            verify_witness(self.snapshot, self.encode(self.request))

    def test_false_attestation(self):
        self.request["chronology_status"] = "TIMESTAMPED"
        with self.assertRaises(ValueError):
            verify_witness(self.snapshot, self.encode(self.request))

    def test_unverified_token(self):
        self.request["external_timestamp_token"] = "fake"
        with self.assertRaises(ValueError):
            verify_witness(self.snapshot, self.encode(self.request))

if __name__ == "__main__":
    unittest.main()
