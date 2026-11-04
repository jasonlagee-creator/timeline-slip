import io
import unittest
from unittest.mock import patch
from scripts.request_timestamp import request_token

class FakeResponse:
    status = 200
    headers = {"Content-Type": "application/timestamp-reply"}
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self, n):
        return b"DER"

class TimestampRequestTests(unittest.TestCase):
    def test_https_required(self):
        for url in ["http://tsa.example/test", "file:///tmp/test", "https://user:pass@tsa.example/test"]:
            with self.assertRaises(ValueError):
                request_token(b"query", url)

    @patch("scripts.request_timestamp.urllib.request.urlopen", return_value=FakeResponse())
    def test_request_is_binary_post(self, urlopen):
        self.assertEqual(request_token(b"query", "https://tsa.example/timestamp"), b"DER")
        req = urlopen.call_args.args[0]
        self.assertEqual(req.get_method(), "POST")
        self.assertEqual(req.data, b"query")

    @patch("scripts.request_timestamp.urllib.request.urlopen")
    def test_wrong_content_type(self, urlopen):
        resp = FakeResponse()
        resp.headers = {"Content-Type": "text/html"}
        urlopen.return_value = resp
        with self.assertRaises(ValueError):
            request_token(b"query", "https://tsa.example/timestamp")

if __name__ == "__main__":
    unittest.main()
