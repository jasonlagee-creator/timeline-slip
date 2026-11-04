#!/usr/bin/env python3
"""Verify TS-001 snapshots; does not establish independent chronology."""
import hashlib
import json
import pathlib
import sys

def verify(raw, sidecar):
    expected = sidecar.strip().split()[0]
    if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
        raise ValueError("Invalid sidecar digest")
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError("Snapshot digest mismatch")
    snapshot = json.loads(raw)
    if snapshot.get("schema") != "timeline-slip-evidence-v1":
        raise ValueError("Unsupported schema")
    comments = snapshot.get("comments")
    if not isinstance(comments, list):
        raise ValueError("Invalid comments collection")
    seen = set()
    for item in comments:
        identifier = item.get("comment_id")
        body = item.get("body")
        if not isinstance(identifier, int) or identifier in seen:
            raise ValueError("Invalid or duplicate comment ID")
        seen.add(identifier)
        if not isinstance(body, str) or hashlib.sha256(body.encode("utf-8")).hexdigest() != item.get("body_sha256"):
            raise ValueError("Comment body digest mismatch")
    return len(comments)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: verify_snapshot.py snapshot.json snapshot.sha256")
    count = verify(pathlib.Path(sys.argv[1]).read_bytes(), pathlib.Path(sys.argv[2]).read_text())
    print(f"PASS: {count} comments verified; chronology not independently established")
