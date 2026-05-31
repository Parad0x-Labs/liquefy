# Liquefy Benchmark Suite Results

Generated against 10,000 lines per dataset.

Search latency = time to find a target string in the compressed archive.

Liquefy uses native columnar grep (no full decompress). All others decompress then scan.

---

## JSON agent logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.50 | 0.01 | 282.81x | 2 | 15 | PASS | 8.1 |
| Zstd L3 | 1.50 | 0.04 | 40.19x | 816 | 1432 | PASS | 3.7 |
| Zstd L9 | 1.50 | 0.04 | 39.42x | 91 | 1677 | PASS | 4.1 |
| Zstd L19 | 1.50 | 0.03 | 53.19x | 1 | 1416 | PASS | 4.1 |
| Zstd L22 | 1.50 | 0.03 | 53.19x | 1 | 1180 | PASS | 4.2 |
| LZ4 | 1.50 | 0.21 | 7.14x | 1453 | 1272 | PASS | 4.8 |
| Brotli Q5 | 1.50 | 0.04 | 40.62x | 63 | 682 | PASS | 5.1 |
| Brotli Q9 | 1.50 | 0.03 | 59.19x | 32 | 750 | PASS | 5.4 |
| Brotli Q11 | 1.50 | 0.02 | 63.69x | 1 | 733 | PASS | 5.0 |
| gzip -6 | 1.50 | 0.11 | 13.21x | 138 | 464 | PASS | 6.4 |
| gzip -9 | 1.50 | 0.11 | 13.49x | 64 | 470 | PASS | 6.1 |

## Payment receipts

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.21 | 0.00 | 875.64x | 9 | 15 | PASS | 6.0 |
| Zstd L3 | 1.21 | 0.03 | 43.59x | 653 | 1324 | PASS | 3.8 |
| Zstd L9 | 1.21 | 0.02 | 49.14x | 95 | 1535 | PASS | 3.8 |
| Zstd L19 | 1.21 | 0.03 | 40.41x | 1 | 1220 | PASS | 4.5 |
| Zstd L22 | 1.21 | 0.03 | 40.18x | 1 | 1149 | PASS | 5.9 |
| LZ4 | 1.21 | 0.18 | 6.84x | 1340 | 1227 | PASS | 6.8 |
| Brotli Q5 | 1.21 | 0.03 | 43.11x | 70 | 705 | PASS | 8.2 |
| Brotli Q9 | 1.21 | 0.03 | 45.28x | 27 | 541 | PASS | 8.8 |
| Brotli Q11 | 1.21 | 0.02 | 48.98x | 0 | 685 | PASS | 6.0 |
| gzip -6 | 1.21 | 0.09 | 13.94x | 121 | 444 | PASS | 6.7 |
| gzip -9 | 1.21 | 0.08 | 14.29x | 70 | 500 | PASS | 6.1 |

## Nginx access logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.93 | 0.10 | 9.46x | 520 | 1162 | PASS | 3.7 |
| Zstd L9 | 0.93 | 0.07 | 13.67x | 70 | 1694 | PASS | 3.5 |
| Zstd L19 | 0.93 | 0.05 | 17.78x | 2 | 1666 | PASS | 3.5 |
| Zstd L22 | 0.93 | 0.05 | 17.78x | 2 | 1354 | PASS | 3.4 |
| LZ4 | 0.93 | 0.17 | 5.34x | 1069 | 1250 | PASS | 3.8 |
| Brotli Q5 | 0.93 | 0.06 | 16.31x | 86 | 524 | PASS | 4.6 |
| Brotli Q9 | 0.93 | 0.03 | 30.10x | 30 | 689 | PASS | 4.4 |
| Brotli Q11 | 0.93 | 0.03 | 32.37x | 0 | 681 | PASS | 4.3 |
| gzip -6 | 0.93 | 0.08 | 11.53x | 77 | 473 | PASS | 5.6 |
| gzip -9 | 0.93 | 0.08 | 11.93x | 62 | 482 | PASS | 5.0 |

## Kubernetes logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.52 | 0.00 | 1341.99x | 7 | 9 | PASS | 6.4 |
| Zstd L3 | 1.52 | 0.00 | 345.69x | 2131 | 2464 | PASS | 3.9 |
| Zstd L9 | 1.52 | 0.00 | 610.29x | 377 | 2952 | PASS | 4.4 |
| Zstd L19 | 1.52 | 0.00 | 718.76x | 10 | 2927 | PASS | 3.8 |
| Zstd L22 | 1.52 | 0.00 | 718.76x | 9 | 3193 | PASS | 3.9 |
| LZ4 | 1.52 | 0.08 | 18.29x | 2663 | 1091 | PASS | 4.2 |
| Brotli Q5 | 1.52 | 0.00 | 993.81x | 229 | 550 | PASS | 6.3 |
| Brotli Q9 | 1.52 | 0.00 | 1034.96x | 215 | 541 | PASS | 5.9 |
| Brotli Q11 | 1.52 | 0.00 | 1198.51x | 5 | 569 | PASS | 5.6 |
| gzip -6 | 1.52 | 0.04 | 33.99x | 126 | 344 | PASS | 6.6 |
| gzip -9 | 1.52 | 0.03 | 49.95x | 78 | 476 | PASS | 6.4 |

## Syslog (RFC 3164)

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.92 | 0.02 | 41.70x | 1030 | 1950 | PASS | 3.3 |
| Zstd L9 | 0.92 | 0.02 | 53.56x | 79 | 1992 | PASS | 3.2 |
| Zstd L19 | 0.92 | 0.02 | 48.23x | 1 | 1761 | PASS | 3.6 |
| Zstd L22 | 0.92 | 0.02 | 48.23x | 1 | 1616 | PASS | 3.6 |
| LZ4 | 0.92 | 0.16 | 5.76x | 1240 | 1375 | PASS | 6.2 |
| Brotli Q5 | 0.92 | 0.02 | 57.56x | 107 | 746 | PASS | 5.5 |
| Brotli Q9 | 0.92 | 0.02 | 59.84x | 26 | 621 | PASS | 4.8 |
| Brotli Q11 | 0.92 | 0.01 | 86.54x | 0 | 771 | PASS | 4.3 |
| gzip -6 | 0.92 | 0.06 | 15.73x | 118 | 535 | PASS | 5.3 |
| gzip -9 | 0.92 | 0.06 | 15.97x | 88 | 501 | PASS | 5.7 |

## PostgreSQL slow query

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.36 | 0.02 | 83.42x | 1 | 18 | PASS | 334.1 |
| Zstd L3 | 1.36 | 0.05 | 29.62x | 822 | 1340 | PASS | 4.1 |
| Zstd L9 | 1.36 | 0.05 | 29.74x | 95 | 1830 | PASS | 4.0 |
| Zstd L19 | 1.36 | 0.04 | 37.67x | 1 | 1425 | PASS | 4.0 |
| Zstd L22 | 1.36 | 0.04 | 37.46x | 1 | 1472 | PASS | 4.0 |
| LZ4 | 1.36 | 0.23 | 5.91x | 1144 | 1235 | PASS | 4.2 |
| Brotli Q5 | 1.36 | 0.04 | 38.41x | 86 | 607 | PASS | 7.1 |
| Brotli Q9 | 1.36 | 0.03 | 40.13x | 30 | 555 | PASS | 5.3 |
| Brotli Q11 | 1.36 | 0.02 | 54.77x | 0 | 791 | PASS | 5.1 |
| gzip -6 | 1.36 | 0.12 | 11.60x | 124 | 468 | PASS | 6.5 |
| gzip -9 | 1.36 | 0.12 | 11.73x | 72 | 421 | PASS | 6.0 |
