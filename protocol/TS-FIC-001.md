# Timeline Slip Phase II — Future-information challenge protocol

Status: PROPOSED EXPERIMENT; NOT EVIDENCE OF TEMPORAL COMMUNICATION
Version: 0.1
Protocol ID: TS-FIC-001

## Purpose
Test whether a sealed submission can correctly specify a high-entropy random target that is generated only after the submission deadline. The experiment does not presume that backward-time information transfer is possible.

## Submission
Submit a UTF-8 message to the designated public TS-001 GitHub issue. Include:
- Protocol: TS-FIC-001
- Challenge-ID: a published unique identifier
- Prediction: exactly 64 lowercase hexadecimal characters (256 bits)
- Optional explanation and signature

A prediction is eligible only if it is publicly captured and independently witnessed **before** the target-generation event. GitHub metadata alone is insufficient. All submissions, including invalid and duplicate submissions, must be retained in the audit log.

## Pre-registration
Before accepting submissions, publish and independently timestamp:
- challenge identifier, opening and closing times in UTC
- target-generation procedure and source of randomness
- independent operator and custody arrangements
- exactly how eligible submissions are selected
- number of allowed attempts and multiplicity correction
- scoring and failure criteria
- how missing data, outages, and disputes are handled

No retroactive modification of those rules is permitted for a registered trial.

## Target generation
After the submission deadline, an independent operator generates 32 cryptographically secure random bytes using a documented and audited process, records the result as 64 lowercase hexadecimal characters, and publishes the target with an independent timestamp and witness attestation. Prefer at least two independently controlled entropy sources with an explicitly specified combination method. The target must not be known or fixed before the submission deadline.

## Scoring
An eligible exact match succeeds for that trial. A single uniform independent 256-bit guess matches with probability 2^-256. With N eligible guesses, the union bound on accidental matches is N/2^256, assuming the target is uniform and independent of the guesses. This does not quantify the probability of time travel. A success requires independent replication and adversarial review of custody and information leakage.

## Evidence
Preserve all original submissions, API responses, snapshot SHA-256 digests, independently signed RFC 3161 receipts (if verified), target-generation logs, witness attestations, and software version identifiers. Do not report a trial as independently witnessed until the witness receipt has been validated.

## Known limitations
- The public GitHub issue is an ordinary communications channel, not a temporal receiver.
- FreeTSA service selection alone does not authenticate its signing chain.
- Any trial conducted before independent custody and verified chronology is a dry run, not a decisive scientific experiment.
- A future AI would still need an unknown physical mechanism to affect historical records.
