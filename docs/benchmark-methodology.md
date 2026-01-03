# Benchmark Methodology

## Overview
This document outlines the standard process used by Parad0x Labs to measure the performance of the Liquefy Conduction Engine. We encourage users to use this methodology to reproduce our internal results.

## Environment Specification
Internal benchmarks are conducted on the following baseline:
*   **Hardware:** AWS c6i.2xlarge (or equivalent 8-core x86_64).
*   **Storage:** local NVMe SSD (io2 or equivalent).
*   **OS:** Hardened Linux (Ubuntu 22.04 LTS).
*   **Container Runtime:** Docker 24.x+.

## Dataset Types
We measure performance against three distinct payload profiles:
1.  **Structured Logs:** Standard JSON or Nginx/Apache logs with high field repetition.
2.  **Infrastructure Telemetry:** High-velocity, low-entropy binary data (e.g. NetFlow).
3.  **Mixed Entropy:** Logs containing binary-in-text blobs (e.g. Hex/Base64).

## Metrics & Reporting
*   **Compression Ratio:** `Original_Size / Compressed_Size`.
*   **Ingest Throughput:** MB/s of raw data processed by the encoder.
*   **Query Latency:** Time from search execution to first match return.
*   **Conduction Speed:** Scanning speed of the Search-Gate across compressed archives.

## How to Reproduce
1.  Prepare a 1GB sample of your target dataset.
2.  Run the `$NULL Sovereign SDK` locally with the `--benchmark` flag.
3.  Report the mean results over 5 consecutive runs to account for JIT warming.

## Disclaimer
**Results vary significantly** based on dataset entropy, hardware specifications, and system utilization. All performance claims are benchmark results, not universal guarantees.

---
© 2026 Parad0x Labs. 🚀

