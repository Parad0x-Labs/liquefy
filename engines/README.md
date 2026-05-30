# Liquefy Engines (MIT)

Format-specific compression codecs that beat zstd on structured log data.

## Architecture

Each codec implements compress/decompress for a specific log format, exploiting structural repetition for higher ratios than general-purpose compressors.

The `orchestrator.py` auto-detects format and routes to the best codec.

## Codecs

| Codec | Log Format | Notes |
|-------|-----------|-------|
| `json_codec/` | JSON / structured logs | Columnar compression. 50%+ better ratio vs zstd L19. Native grep support. |
| `nginx_codec/` | Nginx access logs | Field-aware repetition compression |
| `apache_codec/` | Apache access logs | Template reassembly |
| `syslog_codec/` | Syslog RFC 3164/5424 | RFC-aware frame packing |
| `k8s_codec/` | Kubernetes JSON streams | Nested JSON unflattening |
| `sql_codec/` | PostgreSQL / SQL logs | Query template deduplication |
| `aws_codec/` | AWS CloudTrail / VPC Flow | Event-type columnar packing |
| `universal_codec/` | Any log (fallback) | Entropy-adaptive, auto-fallback |
| `netflow_codec/` | NetFlow v5 | Binary field columnar |
| `vmware_codec/` | VMware ESXi logs | Syslog-variant frame packing |
| `windows_codec/` | Windows EVTX | XML event deduplication |
| `scm_codec/` | GitHub audit logs | JSON-variant columnar |

## Quick Start

```python
from engines.orchestrator import NullOrchestrator

orc = NullOrchestrator()
compressed = orc.compress(open("mylog.jsonl", "rb").read())
restored   = orc.decompress(compressed)
assert restored == open("mylog.jsonl", "rb").read()
```

## Benchmark vs zstd

Run the head-to-head benchmark:
```bash
pip install zstandard
python tools/benchmark.py
```

Results on structured JSON (50k lines): Liquefy **~61x ratio vs zstd ~41x**.
See `REPORTS/UNICORN_BENCHMARK.md` for full results.

## License
MIT — © 2026 Parad0x Labs
