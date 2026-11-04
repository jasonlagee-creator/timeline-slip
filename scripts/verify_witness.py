"""Verify a prepared witness request matches the exact snapshot bytes.

This is an internal consistency check, NOT independent timestamp validation.
"""
import argparse
import hashlib
import json
from pathlib import Path

def verify_witness(snapshot_bytes, request_bytes):
    request = json.loads(request_bytes)
    if request.get("schema") != "timeline-slip-witness-request-v1":
        raise ValueError("Unsupported witness request schema")
    if request.get("digest_algorithm") != "sha256":
        raise ValueError("Unsupported digest")
    if request.get("snapshot_size_bytes") != len(snapshot_bytes):
        raise ValueError("Snapshot size mismatch")
    if request.get("snapshot_sha256") != hashlib.sha256(snapshot_bytes).hexdigest():
        raise ValueError("Snapshot digest mismatch")
    if request.get("chronology_status") != "UNWITNESSED":
        raise ValueError("Unsubstantiated chronology status")
    if request.get("external_timestamp_token") is not None or request.get("independent_custodian_receipt") is not None:
        raise ValueError("Unverified external attestation fields")
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("snapshot", type=Path)
    p.add_argument("witness_request", type=Path)
    args = p.parse_args()
    verify_witness(args.snapshot.read_bytes(), args.witness_request.read_bytes())
    print("PASS: witness request matches snapshot; independent chronology NOT established")

if __name__ == "__main__":
    main()
