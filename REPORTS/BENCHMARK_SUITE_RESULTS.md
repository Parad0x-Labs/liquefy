# Liquefy Benchmark Suite Results

Generated against 10,000 lines per dataset.

Search latency = time to find a target string in the compressed archive.

Liquefy uses native columnar grep (no full decompress). All others decompress then scan.

---

## JSON agent logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy fast(L6) | 1.50 | 0.01 | 225.27x | 25 | 42 | PASS | - |
| Liquefy max(L22) | 1.50 | 0.01 | 282.43x | 2 | 25 | PASS | - |
| Zstd L3 | 1.50 | 0.04 | 40.19x | 326 | 1756 | PASS | - |
| Zstd L9 | 1.50 | 0.04 | 39.42x | 77 | 961 | PASS | - |
| Zstd L19 | 1.50 | 0.03 | 53.19x | 1 | 906 | PASS | - |
| Zstd L22 | 1.50 | 0.03 | 53.19x | 1 | 1466 | PASS | - |
| LZ4 | 1.50 | 0.21 | 7.14x | 881 | 1295 | PASS | - |
| Brotli Q5 | 1.50 | 0.04 | 40.62x | 51 | 361 | PASS | - |
| Brotli Q9 | 1.50 | 0.03 | 59.19x | 37 | 417 | PASS | - |
| Brotli Q11 | 1.50 | 0.02 | 63.69x | 1 | 661 | PASS | - |
| gzip -6 | 1.50 | 0.11 | 13.21x | 122 | 407 | PASS | - |
| gzip -9 | 1.50 | 0.11 | 13.49x | 66 | 389 | PASS | - |

## Payment receipts

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy fast(L6) | 1.21 | 0.00 | 871.85x | 21 | 34 | PASS | - |
| Liquefy max(L22) | 1.21 | 0.00 | 876.27x | 24 | 37 | PASS | - |
| Zstd L3 | 1.21 | 0.03 | 43.59x | 723 | 1340 | PASS | - |
| Zstd L9 | 1.21 | 0.02 | 49.14x | 95 | 1491 | PASS | - |
| Zstd L19 | 1.21 | 0.03 | 40.41x | 1 | 406 | PASS | - |
| Zstd L22 | 1.21 | 0.03 | 40.18x | 1 | 1181 | PASS | - |
| LZ4 | 1.21 | 0.18 | 6.84x | 1263 | 1098 | PASS | - |
| Brotli Q5 | 1.21 | 0.03 | 43.11x | 88 | 592 | PASS | - |
| Brotli Q9 | 1.21 | 0.03 | 45.28x | 29 | 571 | PASS | - |
| Brotli Q11 | 1.21 | 0.02 | 48.98x | 0 | 695 | PASS | - |
| gzip -6 | 1.21 | 0.09 | 13.94x | 122 | 478 | PASS | - |
| gzip -9 | 1.21 | 0.08 | 14.29x | 68 | 477 | PASS | - |

## Nginx access logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.93 | 0.10 | 9.46x | 396 | 622 | PASS | - |
| Zstd L9 | 0.93 | 0.07 | 13.67x | 66 | 895 | PASS | - |
| Zstd L19 | 0.93 | 0.05 | 17.78x | 1 | 1743 | PASS | - |
| Zstd L22 | 0.93 | 0.05 | 17.78x | 1 | 970 | PASS | - |
| LZ4 | 0.93 | 0.17 | 5.34x | 892 | 1219 | PASS | - |
| Brotli Q5 | 0.93 | 0.06 | 16.31x | 83 | 502 | PASS | - |
| Brotli Q9 | 0.93 | 0.03 | 30.10x | 23 | 700 | PASS | - |
| Brotli Q11 | 0.93 | 0.03 | 32.37x | 0 | 543 | PASS | - |
| gzip -6 | 0.93 | 0.08 | 11.53x | 80 | 432 | PASS | - |
| gzip -9 | 0.93 | 0.08 | 11.93x | 58 | 442 | PASS | - |

## Kubernetes logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy fast(L6) | 1.52 | 0.00 | 1113.59x | 23 | 16 | PASS | - |
| Liquefy max(L22) | 1.52 | 0.00 | 1350.31x | 14 | 15 | PASS | - |
| Zstd L3 | 1.52 | 0.00 | 345.69x | 2760 | 3316 | PASS | - |
| Zstd L9 | 1.52 | 0.00 | 610.29x | 363 | 2608 | PASS | - |
| Zstd L19 | 1.52 | 0.00 | 718.76x | 12 | 2678 | PASS | - |
| Zstd L22 | 1.52 | 0.00 | 718.76x | 11 | 2862 | PASS | - |
| LZ4 | 1.52 | 0.08 | 18.29x | 3832 | 1583 | PASS | - |
| Brotli Q5 | 1.52 | 0.00 | 993.81x | 304 | 512 | PASS | - |
| Brotli Q9 | 1.52 | 0.00 | 1034.96x | 210 | 359 | PASS | - |
| Brotli Q11 | 1.52 | 0.00 | 1198.51x | 6 | 575 | PASS | - |
| gzip -6 | 1.52 | 0.04 | 33.99x | 169 | 544 | PASS | - |
| gzip -9 | 1.52 | 0.03 | 49.95x | 86 | 540 | PASS | - |

## Syslog (RFC 3164)

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.92 | 0.02 | 41.70x | 915 | 1913 | PASS | - |
| Zstd L9 | 0.92 | 0.02 | 53.56x | 62 | 1352 | PASS | - |
| Zstd L19 | 0.92 | 0.02 | 48.23x | 1 | 1750 | PASS | - |
| Zstd L22 | 0.92 | 0.02 | 48.23x | 1 | 1720 | PASS | - |
| LZ4 | 0.92 | 0.16 | 5.76x | 1258 | 1415 | PASS | - |
| Brotli Q5 | 0.92 | 0.02 | 57.56x | 106 | 688 | PASS | - |
| Brotli Q9 | 0.92 | 0.02 | 59.84x | 38 | 780 | PASS | - |
| Brotli Q11 | 0.92 | 0.01 | 86.54x | 0 | 805 | PASS | - |
| gzip -6 | 0.92 | 0.06 | 15.73x | 116 | 485 | PASS | - |
| gzip -9 | 0.92 | 0.06 | 15.97x | 81 | 482 | PASS | - |

## PostgreSQL slow query

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy fast(L6) | 1.36 | 0.02 | 66.32x | 20 | 51 | PASS | - |
| Liquefy max(L22) | 1.36 | 0.02 | 83.41x | 1 | 61 | PASS | - |
| Zstd L3 | 1.36 | 0.05 | 29.62x | 843 | 1389 | PASS | - |
| Zstd L9 | 1.36 | 0.05 | 29.74x | 64 | 1398 | PASS | - |
| Zstd L19 | 1.36 | 0.04 | 37.67x | 1 | 1566 | PASS | - |
| Zstd L22 | 1.36 | 0.04 | 37.46x | 1 | 1456 | PASS | - |
| LZ4 | 1.36 | 0.23 | 5.91x | 1152 | 1312 | PASS | - |
| Brotli Q5 | 1.36 | 0.04 | 38.41x | 90 | 724 | PASS | - |
| Brotli Q9 | 1.36 | 0.03 | 40.13x | 29 | 707 | PASS | - |
| Brotli Q11 | 1.36 | 0.02 | 54.77x | 0 | 794 | PASS | - |
| gzip -6 | 1.36 | 0.12 | 11.60x | 133 | 454 | PASS | - |
| gzip -9 | 1.36 | 0.12 | 11.73x | 72 | 439 | PASS | - |
