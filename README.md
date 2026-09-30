# DNSSEC Amplification Study

A large-scale active DNS measurement study examining the amplification risk
posed by DNSSEC-enabled queries across the Tranco top-1M domains.

I conducted this study as part of CSDS 426: Internet Measurement and Analysis, advised by Mark Allman. 

## Overview

DNS amplification attacks exploit the disproportion between small queries
and large responses to overwhelm a victim. DNSSEC introduces cryptographic
records — public keys, signatures, and denial-of-existence records — that
increase this disproportion. This project measures and characterizes that
risk across four DNSSEC query types: `DNSKEY`, `DS`, `RRSIG`, and `NSEC`.

## Key Findings

- Only **6.7%** of top-1M domains are fully DNSSEC signed
- Signed domains produce substantially higher amplification than unsigned ones,
  with worst-case factors of **351×** observed for `RRSIG` queries
- `RRSIG` queries are the highest-risk query type; `DS` and `NSEC` contribute
  negligible additional amplification
- RSA-based zones produce **4–8× higher amplification** than elliptic-curve
  alternatives — the ongoing migration to ECDSA/Ed25519 meaningfully reduces risk

## Documents

| | |
|---|---|
|  [Paper](./CSDS_426_Paper_vta9%20(1).pdf) | Full write-up of methodology, results, and analysis |
|  [Slides](./CSDS%20426%20Final%20Presentation.pdf) | 15-minute presentation overview |

## Methodology

Queries were issued using `dig` with EDNS0 enabled (`+bufsize=4096`) against
Google's public resolver (`8.8.8.8`), targeting all domains in the
[Tranco top-1M list](https://tranco-list.eu/) (February 2026 snapshot).
Data was collected March 28 – April 7, 2026 from a single vantage point.
Amplification factor is computed as:

$$Amplification  \\ Factor = Response \\ Size \\ (bytes) / Query \\ Size \\ (bytes)$$
