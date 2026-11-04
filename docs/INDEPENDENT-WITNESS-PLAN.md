# Timeline Slip — Independent Witness Plan (TRP-01 v0.9 draft)

Status: **Design only**. No external timestamp authority, separate custodian, or temporal receiver is connected.

## Evidence chain
1. Read GitHub Issue #1 comments using read-only credentials; preserve GitHub comment IDs, original bodies, and API timestamps.
2. Compute SHA-256 of exact snapshot bytes. Verify the collector's snapshot and sidecar before export.
3. Request an RFC 3161 timestamp token for the SHA-256 imprint from a separately operated timestamp authority (TSA).
4. Verify the token's signed message imprint, policy, signer certificate chain, validity period, and revocation status under an explicitly documented trust policy.
5. Deliver the snapshot, sidecar, timestamp token, certificate material, and verification report to a **separately administered** custodian.
6. Independently re-fetch and reconcile GitHub source comments. Record edits/deletions and any collection gaps.

## Acceptance tests
- A one-byte mutation to the snapshot is rejected.
- A timestamp token for a different digest is rejected.
- Untrusted or expired signing credentials are rejected according to the chosen verification-time policy.
- A compromised primary GitHub account cannot modify the independent custodian's retained copy.
- A submission received after a preregistered freeze is excluded from scoring.
- A labeled synthetic comment is excluded only by an authenticated, preregistered ID/author combination, not by its text.

## Caveats
An RFC 3161 token proves a digest existed by an authority's claimed signing time under the authority's trust assumptions; it does not establish that the source claim is true or from the future. A second Azure storage account under the same administrative identity is **not** an independent custodian.

## Pending decisions
- TSA provider and trust policy
- Independent custodian organization/account
- Retention term and incident response
- Authenticated external challenge generation
- Security review of public ingestion
