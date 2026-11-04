"""Offline end-to-end test of the evidence and witness consistency pipeline."""
import hashlib
import json
import unittest

from scripts.prepare_witness import prepare
from scripts.verify_snapshot import verify
from scripts.verify_witness import verify_witness
from scripts.classification import classify_comment


class PipelineTests(unittest.TestCase):
    def test_synthetic_submission_round_trip(self):
        comment = {"id": 6623176386, "user": {"login": "jasonlagee-creator"}}
        body = "SYNTHETIC TEST — NOT A TEMPORAL RESPONSE"
        classification = classify_comment(comment)
        snapshot = {
            "schema": "timeline-slip-evidence-v1",
            "comments": [{
                "comment_id": comment["id"],
                "classification": classification,
                "body": body,
                "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest()
            }],
            "external_submission_count": 0
        }
        raw = (json.dumps(snapshot, sort_keys=True) + "\n").encode("utf-8")
        sidecar = hashlib.sha256(raw).hexdigest() + "  snapshot.json"
        self.assertEqual(verify(raw, sidecar), 1)
        request = prepare(raw)
        self.assertTrue(verify_witness(raw, json.dumps(request).encode("utf-8")))
        self.assertEqual(request["chronology_status"], "UNWITNESSED")

    def test_witness_cannot_be_reused_for_modified_snapshot(self):
        raw = b'{"schema":"timeline-slip-evidence-v1","comments":[]}'
        request = json.dumps(prepare(raw)).encode("utf-8")
        with self.assertRaises(ValueError):
            verify_witness(raw + b" ", request)


if __name__ == "__main__":
    unittest.main()
