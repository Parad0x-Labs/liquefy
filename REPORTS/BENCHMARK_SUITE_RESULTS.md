# Liquefy Benchmark Suite Results

Generated against 10,000 lines per dataset.

Search latency = time to find a target string in the compressed archive.

Liquefy uses native columnar grep (no full decompress). All others decompress then scan.

---

## JSON agent logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy fast(L6) | 1.50 | 0.01 | 225.61x | 6 | 11 | PASS | - |
| Liquefy max(L22) | 1.50 | 0.01 | 283.13x | 1 | 21 | PASS | - |
| Zstd L3 | 1.50 | 0.04 | 40.19x | 362 | 819 | PASS | 4.6 |
| Zstd L9 | 1.50 | 0.04 | 39.42x | 31 | 674 | PASS | 5.0 |
| Zstd L19 | 1.50 | 0.03 | 53.19x | 1 | 1193 | PASS | 4.0 |
| Zstd L22 | 1.50 | 0.03 | 53.19x | 1 | 1210 | PASS | 4.0 |
| LZ4 | 1.50 | 0.21 | 7.14x | 1181 | 1314 | PASS | 5.7 |
| Brotli Q5 | 1.50 | 0.04 | 40.62x | 76 | 699 | PASS | 9.6 |
| Brotli Q9 | 1.50 | 0.03 | 59.19x | 42 | 699 | PASS | 7.1 |
| Brotli Q11 | 1.50 | 0.02 | 63.69x | 1 | 610 | PASS | 5.3 |
| gzip -6 | 1.50 | 0.11 | 13.21x | 142 | 440 | PASS | 9.2 |
| gzip -9 | 1.50 | 0.11 | 13.49x | 58 | 503 | PASS | 6.5 |

## Payment receipts

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy fast(L6) | 1.21 | 0.00 | 873.74x | 13 | 19 | PASS | - |
| Liquefy max(L22) | 1.21 | 0.00 | 878.82x | 19 | 22 | PASS | - |
| Zstd L3 | 1.21 | 0.03 | 43.59x | 502 | 921 | PASS | 4.1 |
| Zstd L9 | 1.21 | 0.02 | 49.14x | 79 | 1170 | PASS | 3.7 |
| Zstd L19 | 1.21 | 0.03 | 40.41x | 1 | 1087 | PASS | 4.2 |
| Zstd L22 | 1.21 | 0.03 | 40.18x | 1 | 619 | PASS | 4.0 |
| LZ4 | 1.21 | 0.18 | 6.84x | 844 | 538 | PASS | 4.2 |
| Brotli Q5 | 1.21 | 0.03 | 43.11x | 41 | 225 | PASS | 5.3 |
| Brotli Q9 | 1.21 | 0.03 | 45.28x | 23 | 538 | PASS | 5.3 |
| Brotli Q11 | 1.21 | 0.02 | 48.98x | 0 | 403 | PASS | 5.0 |
| gzip -6 | 1.21 | 0.09 | 13.94x | 110 | 372 | PASS | 6.4 |
| gzip -9 | 1.21 | 0.08 | 14.29x | 68 | 485 | PASS | 6.7 |

## Nginx access logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.93 | 0.10 | 9.46x | 325 | 901 | PASS | 3.9 |
| Zstd L9 | 0.93 | 0.07 | 13.67x | 62 | 1134 | PASS | 4.6 |
| Zstd L19 | 0.93 | 0.05 | 17.78x | 1 | 921 | PASS | 4.1 |
| Zstd L22 | 0.93 | 0.05 | 17.78x | 1 | 966 | PASS | 4.1 |
| LZ4 | 0.93 | 0.17 | 5.34x | 552 | 331 | PASS | 4.1 |
| Brotli Q5 | 0.93 | 0.06 | 16.31x | 35 | 330 | PASS | 5.1 |
| Brotli Q9 | 0.93 | 0.03 | 30.10x | 13 | 238 | PASS | 5.2 |
| Brotli Q11 | 0.93 | 0.03 | 32.37x | 0 | 618 | PASS | 6.1 |
| gzip -6 | 0.93 | 0.08 | 11.53x | 76 | 373 | PASS | 5.9 |
| gzip -9 | 0.93 | 0.08 | 11.93x | 53 | 418 | PASS | 6.2 |

## Kubernetes logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy fast(L6) | 1.52 | 0.00 | 1117.67x | 14 | 8 | PASS | - |
| Liquefy max(L22) | 1.52 | 0.00 | 1347.92x | 9 | 12 | PASS | - |
| Zstd L3 | 1.52 | 0.00 | 345.69x | 2475 | 2590 | PASS | 4.2 |
| Zstd L9 | 1.52 | 0.00 | 610.29x | 292 | 2456 | PASS | 4.5 |
| Zstd L19 | 1.52 | 0.00 | 718.76x | 9 | 2244 | PASS | 3.9 |
| Zstd L22 | 1.52 | 0.00 | 718.76x | 10 | 2383 | PASS | 3.8 |
| LZ4 | 1.52 | 0.08 | 18.29x | 1625 | 519 | PASS | 5.2 |
| Brotli Q5 | 1.52 | 0.00 | 993.81x | 223 | 481 | PASS | 7.3 |
| Brotli Q9 | 1.52 | 0.00 | 1034.96x | 181 | 450 | PASS | 9.6 |
| Brotli Q11 | 1.52 | 0.00 | 1198.51x | 4 | 367 | PASS | 9.6 |
| gzip -6 | 1.52 | 0.04 | 33.99x | 117 | 377 | PASS | 13.5 |
| gzip -9 | 1.52 | 0.03 | 49.95x | 80 | 467 | PASS | 11.5 |

## Syslog (RFC 3164)

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.92 | 0.02 | 41.70x | 717 | 1422 | PASS | 5.0 |
| Zstd L9 | 0.92 | 0.02 | 53.56x | 53 | 842 | PASS | 3.6 |
| Zstd L19 | 0.92 | 0.02 | 48.23x | 1 | 1568 | PASS | 4.1 |
| Zstd L22 | 0.92 | 0.02 | 48.23x | 1 | 1564 | PASS | 4.0 |
| LZ4 | 0.92 | 0.16 | 5.76x | 1284 | 996 | PASS | 5.0 |
| Brotli Q5 | 0.92 | 0.02 | 57.56x | 102 | 710 | PASS | 5.4 |
| Brotli Q9 | 0.92 | 0.02 | 59.84x | 34 | 722 | PASS | 5.6 |
| Brotli Q11 | 0.92 | 0.01 | 86.54x | 0 | 561 | PASS | 5.0 |
| gzip -6 | 0.92 | 0.06 | 15.73x | 106 | 489 | PASS | 6.2 |
| gzip -9 | 0.92 | 0.06 | 15.97x | 89 | 262 | PASS | 7.5 |

## PostgreSQL slow query

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy fast(L6) | 1.36 | 0.02 | 66.43x | 17 | 23 | PASS | - |
| Liquefy max(L22) | 1.36 | 0.02 | 83.44x | 1 | 30 | PASS | - |
| Zstd L3 | 1.36 | 0.05 | 29.62x | 707 | 1412 | PASS | 4.3 |
| Zstd L9 | 1.36 | 0.05 | 29.74x | 81 | 1635 | PASS | 3.9 |
| Zstd L19 | 1.36 | 0.04 | 37.67x | 1 | 1358 | PASS | 4.3 |
| Zstd L22 | 1.36 | 0.04 | 37.46x | 1 | 984 | PASS | 4.0 |
| LZ4 | 1.36 | 0.23 | 5.91x | 486 | 653 | PASS | 4.4 |
| Brotli Q5 | 1.36 | 0.04 | 38.41x | 46 | 582 | PASS | 5.5 |
| Brotli Q9 | 1.36 | 0.03 | 40.13x | 26 | 611 | PASS | 5.0 |
| Brotli Q11 | 1.36 | 0.02 | 54.77x | 1 | 685 | PASS | 5.2 |
| gzip -6 | 1.36 | 0.12 | 11.60x | 122 | 471 | PASS | 6.0 |
| gzip -9 | 1.36 | 0.12 | 11.73x | 70 | 441 | PASS | 7.1 |
