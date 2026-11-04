import pathlib
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from scripts.verify_timestamp_response import verify_timestamp

class TimestampVerificationTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.dir.name)
        self.snapshot = root / "snapshot.json"
        self.response = root / "snapshot.tsr"
        self.ca = root / "trusted-ca.pem"
        for p in (self.snapshot, self.response, self.ca):
            p.write_bytes(b"test")

    def tearDown(self):
        self.dir.cleanup()

    @patch("scripts.verify_timestamp_response.subprocess.run")
    def test_success(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, "Verification: OK\n", "")
        self.assertIn("Verification: OK", verify_timestamp(self.snapshot, self.response, self.ca))
        args = run.call_args.args[0]
        self.assertIn("-CAfile", args)
        self.assertIn("-data", args)

    @patch("scripts.verify_timestamp_response.subprocess.run")
    def test_bad_signature_rejected(self, run):
        run.return_value = subprocess.CompletedProcess([], 1, "", "signature failure")
        with self.assertRaises(ValueError):
            verify_timestamp(self.snapshot, self.response, self.ca)

    @patch("scripts.verify_timestamp_response.subprocess.run")
    def test_missing_positive_verification_rejected(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, "unexpected output", "")
        with self.assertRaises(ValueError):
            verify_timestamp(self.snapshot, self.response, self.ca)

    def test_missing_ca_rejected(self):
        with self.assertRaises(FileNotFoundError):
            verify_timestamp(self.snapshot, self.response, self.ca.parent / "missing.pem")

if __name__ == "__main__":
    unittest.main()
