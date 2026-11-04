# Timeline Slip — Artifact acceptance procedure

## First completed collector run
The first successful manual collector run is TS-001 snapshot #2 (2026-11-03, as reported by the operator's GitHub Actions screenshots). The screenshots show one uploaded artifact and all job steps successful. They do not provide the run ID or artifact digest.

## Independent download and verification
1. Open https://github.com/jasonlagee-creator/timeline-slip/actions/workflows/ts001-collector.yml
2. Open successful run #2 and download its `ts001-evidence-<run-id>` artifact.
3. Extract `snapshot.json` and `snapshot.sha256` without modifying them.
4. Run `python scripts/verify_snapshot.py snapshot.json snapshot.sha256`.
5. Record the run ID, artifact ID, SHA-256 of the ZIP, SHA-256 of `snapshot.json`, verifier output, and retrieval time.
6. Confirm the single synthetic comment ID `6623176386` is marked as a test and the external submission count is zero.
7. Independently archive the original ZIP and its digest outside the GitHub administrative boundary.

## Remaining limitations
GitHub Actions success establishes the configured steps passed; it is not proof of independently witnessed chronology. The original artifact has not yet been independently downloaded and rehashed in this project record. The scheduled six-hour trigger has not been independently confirmed by a successful scheduled run. No temporal communications are established.
