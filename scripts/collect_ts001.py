#!/usr/bin/env python3
"""Read-only collector for public TS-001 GitHub issue comments."""
import hashlib
import json
import os
import pathlib
import urllib.request
from datetime import datetime, timezone

REPO = "jasonlagee-creator/timeline-slip"
ISSUE = 1
OUT = pathlib.Path("evidence")
OUT.mkdir(exist_ok=True)
token = os.environ.get("GITHUB_TOKEN", "")
headers = {"Accept": "application/vnd.github+json", "User-Agent": "timeline-slip-readonly-collector", "X-GitHub-Api-Version": "2022-11-28"}
if token:
    headers["Authorization"] = "Bearer " + token

KNOWN_SYNTHETIC_COMMENT_IDS = {6623176386}

records = []
url = f"https://api.github.com/repos/{REPO}/issues/{ISSUE}/comments?per_page=100&page="
for page in range(1, 101):
    req = urllib.request.Request(url + str(page), headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        data = json.load(response)
    if not isinstance(data, list):
        raise RuntimeError("Unexpected GitHub response")
    for item in data:
        body = item.get("body") or ""
        records.append({
            "comment_id": item["id"],
            "author": (item.get("user") or {}).get("login"),
            "created_at": item.get("created_at"),
            "updated_at": item.get("updated_at"),
            "html_url": item.get("html_url"),
            "classification": "synthetic_test" if item["id"] in KNOWN_SYNTHETIC_COMMENT_IDS and (item.get("user") or {}).get("login") == "jasonlagee-creator" else "unverified_submission",
            "body": body,
            "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest()
        })
    if len(data) < 100:
        break
else:
    raise RuntimeError("Pagination limit reached; fail closed")

records.sort(key=lambda x: x["comment_id"])
snapshot = {
    "schema": "timeline-slip-evidence-v1",
    "source": f"https://github.com/{REPO}/issues/{ISSUE}",
    "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
    "chronology_status": "UNWITNESSED_GITHUB_METADATA",
    "external_submission_count": sum(1 for r in records if r["classification"] != "synthetic_test"),
    "comments": records
}
raw = (json.dumps(snapshot, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
(OUT / "snapshot.json").write_bytes(raw)
(OUT / "snapshot.sha256").write_text(hashlib.sha256(raw).hexdigest() + "  snapshot.json\n", encoding="utf-8")
print(f"Collected {len(records)} comments; SHA-256 {hashlib.sha256(raw).hexdigest()}")
