# Liquefy Benchmark Suite Results

Generated against 10,000 lines per dataset.

Search latency = time to find a target string in the compressed archive.

Liquefy uses native columnar grep (no full decompress). All others decompress then scan.

---

## JSON agent logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.50 | 0.01 | 153.78x | 2 | 18 | PASS | 0.5 |
| Zstd L3 | 1.50 | 0.04 | 40.19x | 546 | 1621 | PASS | 7.1 |
| Zstd L9 | 1.50 | 0.04 | 39.42x | 61 | 899 | PASS | 4.2 |
| Zstd L19 | 1.50 | 0.03 | 53.19x | 1 | 680 | PASS | 4.6 |
| Zstd L22 | 1.50 | 0.03 | 53.19x | 1 | 1432 | PASS | 4.0 |
| LZ4 | 1.50 | 0.21 | 7.14x | 914 | 1135 | PASS | 4.4 |
| Brotli Q5 | 1.50 | 0.04 | 40.62x | 49 | 461 | PASS | 6.1 |
| Brotli Q9 | 1.50 | 0.03 | 59.19x | 31 | 589 | PASS | 9.4 |
| Brotli Q11 | 1.50 | 0.02 | 63.69x | 1 | 478 | PASS | 6.9 |
| gzip -6 | 1.50 | 0.11 | 13.21x | 124 | 412 | PASS | 6.1 |
| gzip -9 | 1.50 | 0.11 | 13.49x | 63 | 376 | PASS | 6.2 |

## Payment receipts

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.21 | 0.00 | 710.39x | 10 | 15 | PASS | 0.1 |
| Zstd L3 | 1.21 | 0.03 | 43.59x | 601 | 1282 | PASS | 3.9 |
| Zstd L9 | 1.21 | 0.02 | 49.14x | 95 | 1406 | PASS | 4.3 |
| Zstd L19 | 1.21 | 0.03 | 40.41x | 1 | 1186 | PASS | 7.7 |
| Zstd L22 | 1.21 | 0.03 | 40.18x | 1 | 1283 | PASS | 4.1 |
| LZ4 | 1.21 | 0.18 | 6.84x | 1448 | 1327 | PASS | 4.9 |
| Brotli Q5 | 1.21 | 0.03 | 43.11x | 75 | 601 | PASS | 5.6 |
| Brotli Q9 | 1.21 | 0.03 | 45.28x | 28 | 536 | PASS | 4.8 |
| Brotli Q11 | 1.21 | 0.02 | 48.98x | 0 | 672 | PASS | 4.9 |
| gzip -6 | 1.21 | 0.09 | 13.94x | 124 | 465 | PASS | 6.7 |
| gzip -9 | 1.21 | 0.08 | 14.29x | 69 | 477 | PASS | 5.4 |

## Nginx access logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.93 | 0.10 | 9.46x | 376 | 997 | PASS | 3.8 |
| Zstd L9 | 0.93 | 0.07 | 13.67x | 69 | 1616 | PASS | 3.4 |
| Zstd L19 | 0.93 | 0.05 | 17.78x | 2 | 1864 | PASS | 3.5 |
| Zstd L22 | 0.93 | 0.05 | 17.78x | 2 | 1877 | PASS | 3.6 |
| LZ4 | 0.93 | 0.17 | 5.34x | 1068 | 1105 | PASS | 3.6 |
| Brotli Q5 | 0.93 | 0.06 | 16.31x | 86 | 684 | PASS | 4.3 |
| Brotli Q9 | 0.93 | 0.03 | 30.10x | 24 | 708 | PASS | 4.9 |
| Brotli Q11 | 0.93 | 0.03 | 32.37x | 0 | 539 | PASS | 4.3 |
| gzip -6 | 0.93 | 0.08 | 11.53x | 78 | 434 | PASS | 6.4 |
| gzip -9 | 0.93 | 0.08 | 11.93x | 60 | 412 | PASS | 5.4 |

## Kubernetes logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.52 | 0.00 | 945.13x | 15 | 29 | PASS | 0.3 |
| Zstd L3 | 1.52 | 0.00 | 345.69x | 2520 | 2855 | PASS | 4.4 |
| Zstd L9 | 1.52 | 0.00 | 610.29x | 374 | 3072 | PASS | 3.8 |
| Zstd L19 | 1.52 | 0.00 | 718.76x | 11 | 2464 | PASS | 3.7 |
| Zstd L22 | 1.52 | 0.00 | 718.76x | 11 | 1798 | PASS | 3.6 |
| LZ4 | 1.52 | 0.08 | 18.29x | 3611 | 1163 | PASS | 4.2 |
| Brotli Q5 | 1.52 | 0.00 | 993.81x | 254 | 358 | PASS | 5.9 |
| Brotli Q9 | 1.52 | 0.00 | 1034.96x | 160 | 548 | PASS | 5.8 |
| Brotli Q11 | 1.52 | 0.00 | 1198.51x | 5 | 519 | PASS | 6.9 |
| gzip -6 | 1.52 | 0.04 | 33.99x | 157 | 243 | PASS | 6.0 |
| gzip -9 | 1.52 | 0.03 | 49.95x | 84 | 548 | PASS | 6.1 |

## Syslog (RFC 3164)

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.92 | 0.02 | 41.70x | 506 | 1339 | PASS | 3.6 |
| Zstd L9 | 0.92 | 0.02 | 53.56x | 79 | 1734 | PASS | 3.4 |
| Zstd L19 | 0.92 | 0.02 | 48.23x | 1 | 1652 | PASS | 4.2 |
| Zstd L22 | 0.92 | 0.02 | 48.23x | 1 | 1232 | PASS | 3.5 |
| LZ4 | 0.92 | 0.16 | 5.76x | 890 | 744 | PASS | 3.6 |
| Brotli Q5 | 0.92 | 0.02 | 57.56x | 99 | 899 | PASS | 4.3 |
| Brotli Q9 | 0.92 | 0.02 | 59.84x | 39 | 795 | PASS | 4.3 |
| Brotli Q11 | 0.92 | 0.01 | 86.54x | 0 | 650 | PASS | 3.9 |
| gzip -6 | 0.92 | 0.06 | 15.73x | 119 | 476 | PASS | 4.8 |
| gzip -9 | 0.92 | 0.06 | 15.97x | 90 | 452 | PASS | 4.7 |

## PostgreSQL slow query

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 1.36 | 0.02 | 82.55x | 1 | 19 | PASS | 329.2 |
| Zstd L3 | 1.36 | 0.05 | 29.62x | 669 | 1456 | PASS | 4.1 |
| Zstd L9 | 1.36 | 0.05 | 29.74x | 66 | 1021 | PASS | 4.0 |
| Zstd L19 | 1.36 | 0.04 | 37.67x | 1 | 1525 | PASS | 4.5 |
| Zstd L22 | 1.36 | 0.04 | 37.46x | 1 | 1544 | PASS | 4.5 |
| LZ4 | 1.36 | 0.23 | 5.91x | 1015 | 1232 | PASS | 4.3 |
| Brotli Q5 | 1.36 | 0.04 | 38.41x | 82 | 566 | PASS | 5.5 |
| Brotli Q9 | 1.36 | 0.03 | 40.13x | 27 | 470 | PASS | 5.4 |
| Brotli Q11 | 1.36 | 0.02 | 54.77x | 0 | 788 | PASS | 5.2 |
| gzip -6 | 1.36 | 0.12 | 11.60x | 132 | 422 | PASS | 7.1 |
| gzip -9 | 1.36 | 0.12 | 11.73x | 72 | 431 | PASS | 6.6 |
