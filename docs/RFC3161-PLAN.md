# RFC 3161 timestamping — implementation boundary

The collector creates `evidence/snapshot.tsq`, an RFC 3161 timestamp **request** containing the SHA-256 digest of `snapshot.json`. This is not a timestamp token.

## Next stage (not configured)
1. Select a reputable external Timestamp Authority (TSA), document its policy, endpoint, certificates and operational independence.
2. Submit the .tsq to that authority through a controlled workflow. Retain the original .tsr response and any associated certificate material.
3. Verify response status, signed message imprint, hash algorithm, certificate chain, extended key usage, policy, and time validity under a defined trust policy.
4. Independently retain the original snapshot, .tsq, .tsr, and verification output.
5. Test tampering, wrong digest, untrusted signer and stale or malformed tokens.

OpenSSL example for creating a request:
```
openssl ts -query -data evidence/snapshot.json -sha256 -cert -out evidence/snapshot.tsq
```

OpenSSL example for verification, **only after** obtaining a genuine .tsr and trusted TSA CA material:
```
openssl ts -verify -data evidence/snapshot.json -in evidence/snapshot.tsr -CAfile trusted-tsa-ca.pem
```

Do not trust an arbitrary certificate supplied with an incoming message as the TSA trust anchor. A valid timestamp indicates an imprint was presented by a claimed time under the TSA's trust assumptions; it does not establish temporal origin.
