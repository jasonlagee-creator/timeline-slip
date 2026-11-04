import hashlib
import unittest
from scripts.prepare_witness import prepare

class WitnessRequestTests(unittest.TestCase):
    def test_digest_matches_original_bytes(self):
        raw = b'{"comments":[]}'
        result = prepare(raw)
        self.assertEqual(result["snapshot_sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(result["snapshot_size_bytes"], len(raw))

    def test_mutation_changes_digest(self):
        self.assertNotEqual(prepare(b"a")["snapshot_sha256"], prepare(b"b")["snapshot_sha256"])

    def test_never_claims_external_timestamp(self):
        result = prepare(b"test")
        self.assertEqual(result["chronology_status"], "UNWITNESSED")
        self.assertIsNone(result["external_timestamp_token"])
        self.assertIsNone(result["independent_custodian_receipt"])

if __name__ == "__main__":
    unittest.main()
