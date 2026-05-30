# Parad0x Labs — Liquefy: Technical Overview

**Project:** Liquefy — Open Source Log Compression and Search Engine
**Status:** Open Source / MIT
**Version:** Python OSS v1.0

---

## 1. What It Is

Liquefy is an open-source (MIT) log compression and search engine. It applies format-specific codecs to compress structured logs significantly better than general-purpose compressors like zstd, while enabling fast columnar search without full decompression.

---

## 2. Architecture

### Hyper-Orchestrator

An auto-routing layer inspects incoming log streams, detects format, and selects the appropriate codec. No manual configuration is required for supported formats.

### 12 Format Codecs

Each codec is tuned to the schema and field distribution of a specific log format:

| Codec | Target Format |
|---|---|
| JSON | Generic structured JSON logs |
| Nginx | Nginx access and error logs |
| Apache | Apache Combined/Common log format |
| Syslog | RFC 3164 / RFC 5424 syslog |
| K8s | Kubernetes pod and event logs |
| SQL | Database query and audit logs |
| AWS CloudTrail | AWS API audit events |
| VPC Flow | AWS VPC Flow Logs |
| Netflow | Netflow v5/v9/IPFIX records |
| VMware | ESXi and vCenter logs |
| GitHub SCM | GitHub webhook and audit logs |
| Windows EVTX | Windows Event Log (EVTX) |

### Codec Internals

Each codec applies format-aware preprocessing: field extraction, dictionary encoding, delta encoding for timestamps and numeric sequences, and run-length encoding for repeated categorical values. This structural encoding stage feeds a final entropy compression pass. The combination is what drives ratio gains over generic compressors.

---

## 3. Key Results

- **Compression ratio:** 50%+ better than zstd level 19 on structured JSON logs.
- **Columnar search:** Decodes only 2-65% of bytes depending on query selectivity, versus 100% for zstd. This enables fast field-level search on compressed archives.
- **Throughput:** Compression and decompression speeds comparable to zstd at equivalent ratio targets.

---

## 4. Docker Decoder Path

A hardened offline recovery image is provided separately from the OSS Python engines. It packages a standalone decoder that reconstructs archives without requiring a full Python environment. The container runs with:

- `--network=none`: No data egress.
- `--read-only`: Immutable filesystem.
- `--cap-drop=ALL`: Minimal Linux capabilities.
- `--user`: Non-root restricted user.

Intended for air-gapped compliance environments and disaster recovery scenarios.

---

## 5. Compliance

- All processing runs locally. No data leaves the machine.
- No telemetry, no cloud calls.
- Suitable for GDPR-regulated data and air-gapped networks.
- Stable CLI contracts and machine-readable JSON output support automated audit logging.

---

## 6. License

MIT. Full source available in the Parad0x Labs repository.
