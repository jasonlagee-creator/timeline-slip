import unittest
from scripts.classification import classify_comment

class ClassificationTests(unittest.TestCase):
    def test_registered_test(self):
        self.assertEqual(classify_comment({"id": 6623176386, "user": {"login": "jasonlagee-creator"}}), "synthetic_test")

    def test_spoofed_body_not_excluded(self):
        self.assertEqual(classify_comment({"id": 900, "user": {"login": "outsider"}, "body": "SYNTHETIC TEST — NOT A TEMPORAL RESPONSE"}), "unverified_submission")

    def test_spoofed_author_not_excluded(self):
        self.assertEqual(classify_comment({"id": 6623176386, "user": {"login": "outsider"}}), "unverified_submission")

    def test_other_owner_comment_not_excluded(self):
        self.assertEqual(classify_comment({"id": 1234, "user": {"login": "jasonlagee-creator"}}), "unverified_submission")

if __name__ == "__main__":
    unittest.main()
