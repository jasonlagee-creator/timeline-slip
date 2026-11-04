import hashlib
import unittest
from unittest.mock import patch
from scripts.freetsa_exchange import fetch_pinned, CERTS, require_approved_pins

class Response:
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, count): return b"certificate-bytes"

class FreeTSAPinningTests(unittest.TestCase):
    @patch("scripts.freetsa_exchange.urllib.request.urlopen", return_value=Response())
    def test_valid_digest(self, _):
        digest = hashlib.sha256(b"certificate-bytes").hexdigest()
        self.assertEqual(fetch_pinned("https://freetsa.org/files/tsa.crt", digest), b"certificate-bytes")

    @patch("scripts.freetsa_exchange.urllib.request.urlopen", return_value=Response())
    def test_mismatch_fails_closed(self, _):
        with self.assertRaises(ValueError):
            fetch_pinned("https://freetsa.org/files/tsa.crt", "0" * 64)

    def test_expected_certificate_pins(self):
        self.assertEqual(len(CERTS), 2)
        for url, digest in CERTS.values():
            self.assertTrue(url.startswith("https://freetsa.org/files/"))
            self.assertIn(len(digest), (0, 64))

    def test_unapproved_pins_fail_closed(self):
        if any(not digest for _, digest in CERTS.values()):
            with self.assertRaises(ValueError):
                require_approved_pins()

if __name__ == "__main__":
    unittest.main()
