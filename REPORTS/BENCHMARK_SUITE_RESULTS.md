# Liquefy Benchmark Suite Results

Generated against 10,000 lines per dataset.

Search latency = time to find a target string in the compressed archive.

Liquefy uses native columnar grep (no full decompress). All others decompress then scan.

---

## JSON agent logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.50 | 0.01 | 282.81x | 2 | 13 | PASS | - |
| Zstd L3 | 1.50 | 0.04 | 40.19x | 635 | 1774 | PASS | - |
| Zstd L9 | 1.50 | 0.04 | 39.42x | 68 | 1727 | PASS | - |
| Zstd L19 | 1.50 | 0.03 | 53.19x | 2 | 773 | PASS | - |
| Zstd L22 | 1.50 | 0.03 | 53.19x | 1 | 1424 | PASS | - |
| LZ4 | 1.50 | 0.21 | 7.14x | 967 | 1376 | PASS | - |
| Brotli Q5 | 1.50 | 0.04 | 40.62x | 73 | 472 | PASS | - |
| Brotli Q9 | 1.50 | 0.03 | 59.19x | 40 | 810 | PASS | - |
| Brotli Q11 | 1.50 | 0.02 | 63.69x | 0 | 491 | PASS | - |
| gzip -6 | 1.50 | 0.11 | 13.21x | 107 | 358 | PASS | - |
| gzip -9 | 1.50 | 0.11 | 13.49x | 68 | 454 | PASS | - |

## Payment receipts

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.21 | 0.00 | 875.64x | 5 | 11 | PASS | - |
| Zstd L3 | 1.21 | 0.03 | 43.59x | 465 | 926 | PASS | - |
| Zstd L9 | 1.21 | 0.02 | 49.14x | 52 | 920 | PASS | - |
| Zstd L19 | 1.21 | 0.03 | 40.41x | 1 | 966 | PASS | - |
| Zstd L22 | 1.21 | 0.03 | 40.18x | 1 | 597 | PASS | - |
| LZ4 | 1.21 | 0.18 | 6.84x | 1398 | 842 | PASS | - |
| Brotli Q5 | 1.21 | 0.03 | 43.11x | 60 | 200 | PASS | - |
| Brotli Q9 | 1.21 | 0.03 | 45.28x | 20 | 632 | PASS | - |
| Brotli Q11 | 1.21 | 0.02 | 48.98x | 0 | 665 | PASS | - |
| gzip -6 | 1.21 | 0.09 | 13.94x | 126 | 451 | PASS | - |
| gzip -9 | 1.21 | 0.08 | 14.29x | 68 | 457 | PASS | - |

## Nginx access logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.93 | 0.10 | 9.46x | 499 | 1043 | PASS | - |
| Zstd L9 | 0.93 | 0.07 | 13.67x | 68 | 1335 | PASS | - |
| Zstd L19 | 0.93 | 0.05 | 17.78x | 2 | 1583 | PASS | - |
| Zstd L22 | 0.93 | 0.05 | 17.78x | 1 | 1678 | PASS | - |
| LZ4 | 0.93 | 0.17 | 5.34x | 1033 | 1107 | PASS | - |
| Brotli Q5 | 0.93 | 0.06 | 16.31x | 87 | 618 | PASS | - |
| Brotli Q9 | 0.93 | 0.03 | 30.10x | 27 | 623 | PASS | - |
| Brotli Q11 | 0.93 | 0.03 | 32.37x | 0 | 540 | PASS | - |
| gzip -6 | 0.93 | 0.08 | 11.53x | 76 | 439 | PASS | - |
| gzip -9 | 0.93 | 0.08 | 11.93x | 60 | 452 | PASS | - |

## Kubernetes logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.52 | 0.00 | 1341.99x | 9 | 11 | PASS | - |
| Zstd L3 | 1.52 | 0.00 | 345.69x | 2563 | 2698 | PASS | - |
| Zstd L9 | 1.52 | 0.00 | 610.29x | 301 | 2784 | PASS | - |
| Zstd L19 | 1.52 | 0.00 | 718.76x | 11 | 2513 | PASS | - |
| Zstd L22 | 1.52 | 0.00 | 718.76x | 11 | 2778 | PASS | - |
| LZ4 | 1.52 | 0.08 | 18.29x | 3824 | 1296 | PASS | - |
| Brotli Q5 | 1.52 | 0.00 | 993.81x | 298 | 494 | PASS | - |
| Brotli Q9 | 1.52 | 0.00 | 1034.96x | 172 | 560 | PASS | - |
| Brotli Q11 | 1.52 | 0.00 | 1198.51x | 5 | 508 | PASS | - |
| gzip -6 | 1.52 | 0.04 | 33.99x | 173 | 446 | PASS | - |
| gzip -9 | 1.52 | 0.03 | 49.95x | 73 | 531 | PASS | - |

## Syslog (RFC 3164)

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.92 | 0.02 | 41.70x | 944 | 1722 | PASS | - |
| Zstd L9 | 0.92 | 0.02 | 53.56x | 75 | 1391 | PASS | - |
| Zstd L19 | 0.92 | 0.02 | 48.23x | 1 | 1573 | PASS | - |
| Zstd L22 | 0.92 | 0.02 | 48.23x | 1 | 1521 | PASS | - |
| LZ4 | 0.92 | 0.16 | 5.76x | 1168 | 1141 | PASS | - |
| Brotli Q5 | 0.92 | 0.02 | 57.56x | 110 | 671 | PASS | - |
| Brotli Q9 | 0.92 | 0.02 | 59.84x | 26 | 700 | PASS | - |
| Brotli Q11 | 0.92 | 0.01 | 86.54x | 0 | 745 | PASS | - |
| gzip -6 | 0.92 | 0.06 | 15.73x | 117 | 475 | PASS | - |
| gzip -9 | 0.92 | 0.06 | 15.97x | 91 | 499 | PASS | - |

## PostgreSQL slow query

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.36 | 0.02 | 83.42x | 1 | 16 | PASS | - |
| Zstd L3 | 1.36 | 0.05 | 29.62x | 605 | 776 | PASS | - |
| Zstd L9 | 1.36 | 0.05 | 29.74x | 54 | 904 | PASS | - |
| Zstd L19 | 1.36 | 0.04 | 37.67x | 1 | 1083 | PASS | - |
| Zstd L22 | 1.36 | 0.04 | 37.46x | 1 | 1422 | PASS | - |
| LZ4 | 1.36 | 0.23 | 5.91x | 1064 | 1206 | PASS | - |
| Brotli Q5 | 1.36 | 0.04 | 38.41x | 86 | 653 | PASS | - |
| Brotli Q9 | 1.36 | 0.03 | 40.13x | 24 | 620 | PASS | - |
| Brotli Q11 | 1.36 | 0.02 | 54.77x | 0 | 613 | PASS | - |
| gzip -6 | 1.36 | 0.12 | 11.60x | 130 | 404 | PASS | - |
| gzip -9 | 1.36 | 0.12 | 11.73x | 70 | 316 | PASS | - |
