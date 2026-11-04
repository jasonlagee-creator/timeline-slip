"""Create a deterministic witness request from a captured snapshot.

This does NOT timestamp evidence. It prepares a SHA-256 imprint for an independent
RFC 3161 timestamp authority or separate custodian.
"""
import argparse
import hashlib
import json
from pathlib import Path

def prepare(snapshot_bytes):
    return {
        "schema": "timeline-slip-witness-request-v1",
        "digest_algorithm": "sha256",
        "snapshot_sha256": hashlib.sha256(snapshot_bytes).hexdigest(),
        "snapshot_size_bytes": len(snapshot_bytes),
        "external_timestamp_token": None,
        "independent_custodian_receipt": None,
        "chronology_status": "UNWITNESSED"
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--output", type=Path, default=Path("witness-request.json"))
    args = parser.parse_args()
    data = prepare(args.snapshot.read_bytes())
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Witness request prepared: {data['snapshot_sha256']}; no timestamp acquired")

if __name__ == "__main__":
    main()
