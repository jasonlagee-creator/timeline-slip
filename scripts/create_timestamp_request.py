#!/usr/bin/env python3
"""Generate an RFC 3161 timestamp request for snapshot.json.

A .tsq is only a REQUEST, not a signed timestamp token or proof of chronology.
"""
import argparse
import hashlib
import pathlib
import subprocess

def make_request(snapshot, output):
    data = pathlib.Path(snapshot).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    command = ["openssl", "ts", "-query", "-sha256", "-digest", digest,
               "-cert", "-out", str(output)]
    subprocess.run(command, check=True, capture_output=True, text=True)
    return digest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    digest = make_request(args.snapshot, args.output)
    print(f"RFC 3161 request prepared for SHA-256 {digest}. No TSA response obtained.")

if __name__ == "__main__":
    main()
