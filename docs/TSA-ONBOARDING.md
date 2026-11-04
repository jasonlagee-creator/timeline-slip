# External timestamp authority onboarding — TRP-01 v0.10

Status: **Not connected**. The client is implemented, but no external TSA response has been obtained or independently verified.

## Selection requirements
- Published HTTPS RFC 3161 endpoint and documented service policy
- Authenticated TSA certificate chain from a separately trusted source
- Timestamping extended key usage and documented revocation/renewal process
- Stable availability, clear retention and pricing terms
- Separate administrative control from the Timeline Slip GitHub account

## Controlled manual test
1. Download the original snapshot artifact and verify its snapshot.sha256.
2. Generate the RFC 3161 request using `python scripts/create_timestamp_request.py snapshot.json --output snapshot.tsq`.
3. Select and authenticate a TSA endpoint and its certificate trust anchor independently.
4. Run `python scripts/request_timestamp.py --query snapshot.tsq --endpoint https://YOUR-VERIFIED-TSA-ENDPOINT --response snapshot.tsr`.
5. Verify using `python scripts/verify_timestamp_response.py --snapshot snapshot.json --response snapshot.tsr --ca-file YOUR-TRUSTED-TSA-CA.pem`.
6. Archive the original snapshot, query, response, CA fingerprint, verification logs, and UTC retrieval metadata with a separately administered custodian.

**Security gate:** Do not place arbitrary TSA certificates or endpoints supplied by unverified submitters into the trusted configuration. Do not enable automatic outbound timestamping before an independent endpoint and certificate review.

## Evidence meaning
Successful verification establishes that a trusted TSA signed a matching message imprint under its clock and policy. It does not establish that the underlying historical claim is true, that the message originated in the future, or that a timeline changed.
