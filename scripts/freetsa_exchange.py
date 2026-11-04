#!/usr/bin/env python3
"""FreeTSA RFC 3161 exchange with published certificate fingerprint pins.

A verified timestamp is evidence of a signed imprint, not temporal communication.
"""
import argparse
import hashlib
import os
import pathlib
import urllib.request

from request_timestamp import request_token
from verify_timestamp_response import verify_timestamp

TSA = "https://freetsa.org/tsr"
CERTS = {
    "tsa.crt": ("https://freetsa.org/files/tsa.crt", os.environ.get("FREETSA_TSA_CERT_SHA256", "")),
    "cacert.pem": ("https://freetsa.org/files/cacert.pem", os.environ.get("FREETSA_CA_CERT_SHA256", ""))
}

def require_approved_pins():
    for name, (_, fingerprint) in CERTS.items():
        if len(fingerprint) != 64 or any(ch not in "0123456789abcdef" for ch in fingerprint):
            raise ValueError(f"Missing approved SHA-256 pin for {name}; no timestamp request sent")


def fetch_pinned(url, expected, maximum=65536):
    req = urllib.request.Request(url, headers={"User-Agent": "Timeline-Slip-TRP-01/0.11"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = resp.read(maximum + 1)
    if not data or len(data) > maximum:
        raise ValueError("Certificate size invalid")
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("Certificate fingerprint mismatch; fail closed")
    return data

def exchange(directory):
    directory = pathlib.Path(directory)
    query = directory / "snapshot.tsq"
    snapshot = directory / "snapshot.json"
    if not query.is_file() or not snapshot.is_file():
        raise FileNotFoundError("snapshot.json and snapshot.tsq required")
    require_approved_pins()
    for name, (url, fingerprint) in CERTS.items():
        (directory / name).write_bytes(fetch_pinned(url, fingerprint))
    response = directory / "snapshot.tsr"
    response.write_bytes(request_token(query.read_bytes(), TSA))
    result = verify_timestamp(snapshot, response, directory / "cacert.pem", directory / "tsa.crt")
    (directory / "tsa-verification.txt").write_text(result + "\nChronology: independently signed imprint; no temporal-origin claim.\n")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default="evidence")
    args = parser.parse_args()
    print(exchange(args.directory))
