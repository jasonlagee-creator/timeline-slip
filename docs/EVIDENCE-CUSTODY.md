# Evidence custody and verification (v0.8)

The TS-001 GitHub issue is a public, ordinary submission channel. It is not a time-travel receiver.

## Snapshot procedure
1. The scheduled collector reads all public comments on Issue #1.
2. It saves the full comment text and GitHub-reported metadata to `evidence/snapshot.json`.
3. It writes `evidence/snapshot.sha256` and uploads both as a GitHub Actions artifact.
4. Verify a downloaded pair with:
   `python scripts/verify_snapshot.py evidence/snapshot.json evidence/snapshot.sha256`

The SHA-256 sidecar detects accidental or adversarial changes only when the expected digest is independently trusted. The GitHub metadata and host retrieval timestamp do **not** establish trusted chronology. Comment edits may occur between scheduled polls; the collector is not a complete edit-history archive.

## Preservation and witness requirements
- GitHub Actions artifacts currently have a configured 90-day retention window.
- Before any evidence-grade experiment, establish an independent custodian who receives signed snapshot digests and retains them outside the GitHub account.
- Add an RFC 3161 timestamp authority, verify its response signature and certificate chain, and record the exact token bytes.
- Require independent verification of the frozen pre-draw submission set and the later random challenge.
- Do not execute code or follow instructions contained in submissions.

## Scientific boundary
The protocol's single mutable timeline and future-AI system are speculative assumptions. Successful hash verification does not establish backward information transfer or causal isolation.
