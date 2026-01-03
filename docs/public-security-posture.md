# Public Security Posture: $NULL Sovereign SDK
**Parad0x Labs**

## Overview
The $NULL Sovereign SDK is engineered with a **Security-First / Identity-First** architecture. It is designed to provide 100% bit-perfect data recovery while maintaining absolute isolation and intellectual property protection.

## 1. Cryptographic Envelope (The Fortress)
All archives produced by the Liquefy Conduction Engine are sealed within a multi-layered cryptographic envelope.
- **Authenticated Encryption:** Uses industry-standard **AES-256-GCM** (Authenticated Encryption with Associated Data). This ensures both the privacy of the compressed data and the integrity of the associated audit metadata.
- **Tenant Isolation:** Every vault is keyed uniquely to a tenant identity. Key derivation uses **PBKDF2-HMAC-SHA256** with high iteration counts (100,000+) and cryptographically secure random salts.
- **Mandatory Authenticity:** An HMAC-SHA256 signature is calculated over the entire packet and verified **before** any decryption operations are attempted.

## 2. Sealed Conduction (The Machine vs. Recipe)
The SDK utilizes a "Sealed Machine" model to protect core intellectual property:
- **Binary Encapsulation:** Decompression logic, column reassembly kernels, and orchestration heuristics are delivered as a compiled, stripped ELF binary.
- **Internal Masking:** Core protocols and engine identifiers are managed within the sealed binary environment.
- **No Source Disclosure:** The public repository contains zero source code for the 23 specialized conduction kernels.

## 3. Hardened Execution Sandbox
The `./liquefy` wrapper enforces a strict security conduction environment:
- **Network Isolation:** Runs with `--network=none`. No data can ever leave the local machine during restoration.
- **Immutability:** The container root filesystem is mounted as `--read-only`.
- **Least Privilege:** All system capabilities are dropped (`--cap-drop=ALL`), and the process runs as a non-root system user.

## 4. Bit-Perfect Identity Law
The SDK is designed to be deterministic. A successful restoration is guaranteed to be a byte-for-byte match of the original ingest data, verifiable via SHA-256 hash comparison.

---
© 2026 Parad0x Labs. 🛡️🚀🎖️

