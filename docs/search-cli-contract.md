# Search CLI Contract (Public)

## Overview
This document defines the stable interface for searching `.null` archives via the $NULL Sovereign SDK and sealed decoder appliances.

## Commands
```bash
search <archive> --query "<expr>" [--json] [--limit N] [--context N]
```

### Parameters
*   `<archive>`: Path to the target `.null` or `.liq` file.
*   `--query "<expr>"`: The search expression (supports token match, field filters, and basic regex).
*   `--json`: (Optional) Returns output in a stable JSON schema for automation.
*   `--limit N`: (Optional) Stop searching after N matches.
*   `--context N`: (Optional) Show N lines of context around each match.

## Output Policy
*   **Default:** Human-readable matches with highlighted tokens.
*   **JSON Schema:** A stable array of match objects including offset, timestamp (if available), and payload.

## Exit Codes
To facilitate automation and error handling, the decoder uses the following stable exit codes:

| Code | Meaning | Description |
| :--- | :--- | :--- |
| **0** | Success | Query completed successfully. |
| **10** | Corruption | Integrity failure detected in the archive. |
| **11** | License Invalid | Required license missing or expired (Enterprise Engine only). |
| **12** | Unsupported | Format or version mismatch. |
| **13** | Internal Error | Unexpected failure (no sensitive details disclosed). |

---
© 2026 Parad0x Labs. 🚀

