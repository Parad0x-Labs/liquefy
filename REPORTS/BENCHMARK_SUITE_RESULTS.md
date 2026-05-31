# Liquefy Benchmark Suite Results

Generated against 10,000 lines per dataset.

Search latency = time to find a target string in the compressed archive.

Liquefy uses native columnar grep (no full decompress). All others decompress then scan.

---

## JSON agent logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.50 | 0.01 | 283.13x | 2 | 18 | PASS | - |
| Zstd L3 | 1.50 | 0.04 | 40.19x | 734 | 1667 | PASS | - |
| Zstd L9 | 1.50 | 0.04 | 39.42x | 63 | 781 | PASS | - |
| Zstd L19 | 1.50 | 0.03 | 53.19x | 2 | 735 | PASS | - |
| Zstd L22 | 1.50 | 0.03 | 53.19x | 1 | 1497 | PASS | - |
| LZ4 | 1.50 | 0.21 | 7.14x | 922 | 1348 | PASS | - |
| Brotli Q5 | 1.50 | 0.04 | 40.62x | 58 | 630 | PASS | - |
| Brotli Q9 | 1.50 | 0.03 | 59.19x | 35 | 345 | PASS | - |
| Brotli Q11 | 1.50 | 0.02 | 63.69x | 1 | 594 | PASS | - |
| gzip -6 | 1.50 | 0.11 | 13.21x | 129 | 461 | PASS | - |
| gzip -9 | 1.50 | 0.11 | 13.49x | 66 | 489 | PASS | - |

## Payment receipts

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.21 | 0.00 | 878.82x | 15 | 23 | PASS | - |
| Zstd L3 | 1.21 | 0.03 | 43.59x | 749 | 1420 | PASS | - |
| Zstd L9 | 1.21 | 0.02 | 49.14x | 98 | 1462 | PASS | - |
| Zstd L19 | 1.21 | 0.03 | 40.41x | 1 | 781 | PASS | - |
| Zstd L22 | 1.21 | 0.03 | 40.18x | 1 | 1225 | PASS | - |
| LZ4 | 1.21 | 0.18 | 6.84x | 1432 | 1449 | PASS | - |
| Brotli Q5 | 1.21 | 0.03 | 43.11x | 84 | 692 | PASS | - |
| Brotli Q9 | 1.21 | 0.03 | 45.28x | 23 | 691 | PASS | - |
| Brotli Q11 | 1.21 | 0.02 | 48.98x | 0 | 702 | PASS | - |
| gzip -6 | 1.21 | 0.09 | 13.94x | 116 | 502 | PASS | - |
| gzip -9 | 1.21 | 0.08 | 14.29x | 67 | 448 | PASS | - |

## Nginx access logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.93 | 0.10 | 9.46x | 378 | 1040 | PASS | - |
| Zstd L9 | 0.93 | 0.07 | 13.67x | 62 | 1318 | PASS | - |
| Zstd L19 | 0.93 | 0.05 | 17.78x | 1 | 1929 | PASS | - |
| Zstd L22 | 0.93 | 0.05 | 17.78x | 1 | 1883 | PASS | - |
| LZ4 | 0.93 | 0.17 | 5.34x | 1065 | 1404 | PASS | - |
| Brotli Q5 | 0.93 | 0.06 | 16.31x | 85 | 654 | PASS | - |
| Brotli Q9 | 0.93 | 0.03 | 30.10x | 26 | 431 | PASS | - |
| Brotli Q11 | 0.93 | 0.03 | 32.37x | 0 | 632 | PASS | - |
| gzip -6 | 0.93 | 0.08 | 11.53x | 76 | 446 | PASS | - |
| gzip -9 | 0.93 | 0.08 | 11.93x | 58 | 507 | PASS | - |

## Kubernetes logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.52 | 0.00 | 1347.92x | 13 | 14 | PASS | - |
| Zstd L3 | 1.52 | 0.00 | 345.69x | 2749 | 3095 | PASS | - |
| Zstd L9 | 1.52 | 0.00 | 610.29x | 353 | 2688 | PASS | - |
| Zstd L19 | 1.52 | 0.00 | 718.76x | 11 | 1949 | PASS | - |
| Zstd L22 | 1.52 | 0.00 | 718.76x | 12 | 1356 | PASS | - |
| LZ4 | 1.52 | 0.08 | 18.29x | 2791 | 924 | PASS | - |
| Brotli Q5 | 1.52 | 0.00 | 993.81x | 214 | 547 | PASS | - |
| Brotli Q9 | 1.52 | 0.00 | 1034.96x | 211 | 546 | PASS | - |
| Brotli Q11 | 1.52 | 0.00 | 1198.51x | 6 | 492 | PASS | - |
| gzip -6 | 1.52 | 0.04 | 33.99x | 171 | 501 | PASS | - |
| gzip -9 | 1.52 | 0.03 | 49.95x | 78 | 258 | PASS | - |

## Syslog (RFC 3164)

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.92 | 0.02 | 41.70x | 515 | 1343 | PASS | - |
| Zstd L9 | 0.92 | 0.02 | 53.56x | 66 | 1364 | PASS | - |
| Zstd L19 | 0.92 | 0.02 | 48.23x | 1 | 1335 | PASS | - |
| Zstd L22 | 0.92 | 0.02 | 48.23x | 1 | 1406 | PASS | - |
| LZ4 | 0.92 | 0.16 | 5.76x | 1182 | 1288 | PASS | - |
| Brotli Q5 | 0.92 | 0.02 | 57.56x | 109 | 592 | PASS | - |
| Brotli Q9 | 0.92 | 0.02 | 59.84x | 35 | 524 | PASS | - |
| Brotli Q11 | 0.92 | 0.01 | 86.54x | 0 | 673 | PASS | - |
| gzip -6 | 0.92 | 0.06 | 15.73x | 113 | 478 | PASS | - |
| gzip -9 | 0.92 | 0.06 | 15.97x | 91 | 514 | PASS | - |

## PostgreSQL slow query

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.36 | 0.02 | 83.44x | 1 | 35 | PASS | - |
| Zstd L3 | 1.36 | 0.05 | 29.62x | 847 | 1395 | PASS | - |
| Zstd L9 | 1.36 | 0.05 | 29.74x | 90 | 1423 | PASS | - |
| Zstd L19 | 1.36 | 0.04 | 37.67x | 1 | 1434 | PASS | - |
| Zstd L22 | 1.36 | 0.04 | 37.46x | 1 | 870 | PASS | - |
| LZ4 | 1.36 | 0.23 | 5.91x | 776 | 754 | PASS | - |
| Brotli Q5 | 1.36 | 0.04 | 38.41x | 55 | 385 | PASS | - |
| Brotli Q9 | 1.36 | 0.03 | 40.13x | 21 | 546 | PASS | - |
| Brotli Q11 | 1.36 | 0.02 | 54.77x | 0 | 680 | PASS | - |
| gzip -6 | 1.36 | 0.12 | 11.60x | 109 | 309 | PASS | - |
| gzip -9 | 1.36 | 0.12 | 11.73x | 65 | 414 | PASS | - |
