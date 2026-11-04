#!/usr/bin/env python3
"""Verify an RFC 3161 timestamp response against a snapshot and trusted TSA CA.

A successful verification proves a TSA signed a matching imprint under the supplied
trust configuration. It does not prove temporal origin of the snapshot.
"""
import argparse
import pathlib
import subprocess

def verify_timestamp(snapshot, response, ca_file, untrusted=None):
    for path in [snapshot, response, ca_file]:
        if not pathlib.Path(path).is_file():
            raise FileNotFoundError(path)
    command = ["openssl", "ts", "-verify", "-data", str(snapshot),
               "-in", str(response), "-CAfile", str(ca_file)]
    if untrusted:
        command.extend(["-untrusted", str(untrusted)])
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise ValueError("TSA verification failed: " + (completed.stderr or completed.stdout).strip())
    if "Verification: OK" not in completed.stdout:
        raise ValueError("OpenSSL did not confirm successful verification")
    return completed.stdout.strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", required=True, type=pathlib.Path)
    parser.add_argument("--response", required=True, type=pathlib.Path)
    parser.add_argument("--ca-file", required=True, type=pathlib.Path)
    parser.add_argument("--untrusted", type=pathlib.Path)
    args = parser.parse_args()
    print(verify_timestamp(args.snapshot, args.response, args.ca_file, args.untrusted))
    print("Matching signed TSA response verified; temporal origin NOT established.")

if __name__ == "__main__":
    main()
