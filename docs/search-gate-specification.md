# 🔍 Search-Gate Specification (v3.9)

## Overview
Liquefy v3.9 introduces **Search-Gate**, a high-performance query interface that operates directly on compressed/encrypted `.null` archives. This allows for sub-second data retrieval without the overhead of full decompression.

## Core Principles

1.  **Bloom-Indexed Pruning:** Every `.null` archive contains a Bloom filter index. The Search-Gate uses this index to skip ~98% of data blocks that do not contain the search term.
2.  **Bytecode Execution:** Queries are compiled into optimized bytecode and executed inside the hardened conduction environment.
3.  **Zero-Knowledge Search:** When encrypted, the Search-Gate can identify matching blocks using deterministic tokens without exposing the full plaintext of the archive.

## CLI Contract

The $NULL Sovereign SDK exposes the search interface via the following command:

```bash
./liquefy search <file.null> --query "status=500" --limit 100
```

### Supported Query Semantics
*   **Token Match:** `"ERROR"` or `"404"`
*   **Field Filter:** `"status=500"` or `"host=worker-01"`
*   **Range Query:** `"time > 2025-01-01"` (Standard ISO-8601)
*   **Regex:** `"regex:.*fatal.*"`

## Performance Claims
*   **Latency:** < 500ms for typical filtered queries on 1GB+ archives.
*   **Throughput:** Up to 300MB/s conduction speed during scan.
*   **CPU Impact:** Minimal, due to Bloom-based block skipping.

---
© 2026 Parad0x Labs. 🚀

