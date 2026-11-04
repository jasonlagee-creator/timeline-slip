#!/usr/bin/env python3
"""Obtain RFC 3161 timestamp response from an explicitly configured HTTPS TSA.

The returned token is untrusted until separately verified against a pinned trust
anchor and the original snapshot. Never send the snapshot itself to the TSA.
"""
import argparse
import pathlib
import urllib.parse
import urllib.request

def request_token(query_bytes, endpoint, max_bytes=262144):
    parsed = urllib.parse.urlparse(endpoint)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("An HTTPS TSA endpoint without embedded credentials is required")
    req = urllib.request.Request(
        endpoint, data=query_bytes, method="POST",
        headers={"Content-Type": "application/timestamp-query",
                 "Accept": "application/timestamp-reply",
                 "User-Agent": "Timeline-Slip-TRP-01/0.10"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        if resp.status != 200:
            raise ValueError("Unexpected TSA HTTP status")
        content_type = resp.headers.get("Content-Type", "").split(";")[0].strip().lower()
        if content_type != "application/timestamp-reply":
            raise ValueError("Unexpected TSA content type")
        data = resp.read(max_bytes + 1)
        if not data or len(data) > max_bytes:
            raise ValueError("Invalid TSA response size")
        return data

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--query", required=True, type=pathlib.Path)
    p.add_argument("--endpoint", required=True)
    p.add_argument("--response", required=True, type=pathlib.Path)
    a = p.parse_args()
    token = request_token(a.query.read_bytes(), a.endpoint)
    a.response.write_bytes(token)
    print("Unverified TSA response saved. Run verify_timestamp_response.py with trusted CA material.")

if __name__ == "__main__":
    main()
