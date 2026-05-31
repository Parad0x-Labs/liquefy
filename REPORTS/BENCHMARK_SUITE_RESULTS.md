# Liquefy Benchmark Suite Results

Generated against 5,000 lines per dataset.

Search latency = time to find a target string in the compressed archive.

Liquefy uses native columnar grep (no full decompress). All others decompress then scan.

---

## JSON agent logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 0.75 | 0.02 | 33.60x | 1 | 22 | PASS | 0.4 |
| Zstd L3 | 0.75 | 0.02 | 37.69x | 204 | 1129 | PASS | 2.1 |
| Zstd L9 | 0.75 | 0.02 | 36.35x | 74 | 1114 | PASS | 2.3 |
| Zstd L19 | 0.75 | 0.02 | 46.50x | 2 | 911 | PASS | 2.4 |
| Zstd L22 | 0.75 | 0.02 | 46.50x | 1 | 994 | PASS | 2.5 |
| LZ4 | 0.75 | 0.11 | 7.14x | 1372 | 1401 | PASS | 2.0 |
| Brotli Q5 | 0.75 | 0.02 | 45.38x | 92 | 399 | PASS | 2.6 |
| Brotli Q9 | 0.75 | 0.01 | 55.44x | 38 | 723 | PASS | 3.0 |
| Brotli Q11 | 0.75 | 0.01 | 58.85x | 1 | 822 | PASS | 3.7 |
| gzip -6 | 0.75 | 0.06 | 13.16x | 133 | 328 | PASS | 4.1 |
| gzip -9 | 0.75 | 0.06 | 13.41x | 69 | 465 | PASS | 3.2 |

## Payment receipts

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 0.60 | 0.01 | 65.59x | 2 | 20 | PASS | 0.2 |
| Zstd L3 | 0.60 | 0.01 | 40.47x | 643 | 1311 | PASS | 1.9 |
| Zstd L9 | 0.60 | 0.01 | 49.77x | 78 | 984 | PASS | 1.9 |
| Zstd L19 | 0.60 | 0.02 | 40.19x | 1 | 1244 | PASS | 1.8 |
| Zstd L22 | 0.60 | 0.02 | 39.72x | 1 | 1292 | PASS | 1.8 |
| LZ4 | 0.60 | 0.09 | 6.81x | 1528 | 1348 | PASS | 1.9 |
| Brotli Q5 | 0.60 | 0.01 | 44.42x | 102 | 637 | PASS | 2.3 |
| Brotli Q9 | 0.60 | 0.01 | 45.59x | 34 | 760 | PASS | 2.7 |
| Brotli Q11 | 0.60 | 0.01 | 49.21x | 0 | 743 | PASS | 3.3 |
| gzip -6 | 0.60 | 0.04 | 13.92x | 128 | 502 | PASS | 3.2 |
| gzip -9 | 0.60 | 0.04 | 14.23x | 74 | 475 | PASS | 2.6 |

## Nginx access logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.46 | 0.05 | 9.30x | 433 | 948 | PASS | 1.9 |
| Zstd L9 | 0.46 | 0.04 | 12.89x | 80 | 1528 | PASS | 1.8 |
| Zstd L19 | 0.46 | 0.03 | 16.67x | 2 | 1456 | PASS | 1.7 |
| Zstd L22 | 0.46 | 0.03 | 16.67x | 1 | 1752 | PASS | 1.8 |
| LZ4 | 0.46 | 0.09 | 5.31x | 1000 | 1331 | PASS | 1.8 |
| Brotli Q5 | 0.46 | 0.03 | 15.65x | 84 | 590 | PASS | 2.2 |
| Brotli Q9 | 0.46 | 0.02 | 27.78x | 31 | 653 | PASS | 2.1 |
| Brotli Q11 | 0.46 | 0.02 | 30.66x | 0 | 388 | PASS | 2.2 |
| gzip -6 | 0.46 | 0.04 | 11.33x | 77 | 385 | PASS | 2.5 |
| gzip -9 | 0.46 | 0.04 | 11.71x | 56 | 379 | PASS | 2.5 |

## Kubernetes logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 0.76 | 0.00 | 475.81x | 14 | 29 | PASS | 0.1 |
| Zstd L3 | 0.76 | 0.00 | 175.71x | 1494 | 3084 | PASS | 1.8 |
| Zstd L9 | 0.76 | 0.00 | 314.20x | 201 | 3476 | PASS | 1.9 |
| Zstd L19 | 0.76 | 0.00 | 370.92x | 6 | 3214 | PASS | 1.9 |
| Zstd L22 | 0.76 | 0.00 | 370.92x | 6 | 3066 | PASS | 3.4 |
| LZ4 | 0.76 | 0.04 | 18.05x | 3850 | 1476 | PASS | 3.9 |
| Brotli Q5 | 0.76 | 0.00 | 481.52x | 293 | 515 | PASS | 4.0 |
| Brotli Q9 | 0.76 | 0.00 | 515.38x | 156 | 605 | PASS | 3.4 |
| Brotli Q11 | 0.76 | 0.00 | 599.25x | 3 | 550 | PASS | 4.7 |
| gzip -6 | 0.76 | 0.02 | 33.43x | 173 | 412 | PASS | 3.5 |
| gzip -9 | 0.76 | 0.02 | 48.58x | 86 | 516 | PASS | 3.2 |

## Syslog (RFC 3164)

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.46 | 0.02 | 29.28x | 397 | 1291 | PASS | 2.3 |
| Zstd L9 | 0.46 | 0.01 | 42.47x | 84 | 1809 | PASS | 2.0 |
| Zstd L19 | 0.46 | 0.01 | 41.28x | 1 | 1680 | PASS | 1.8 |
| Zstd L22 | 0.46 | 0.01 | 41.28x | 1 | 1648 | PASS | 1.9 |
| LZ4 | 0.46 | 0.08 | 5.75x | 1156 | 1267 | PASS | 2.1 |
| Brotli Q5 | 0.46 | 0.01 | 50.42x | 102 | 689 | PASS | 2.1 |
| Brotli Q9 | 0.46 | 0.01 | 53.84x | 35 | 684 | PASS | 1.9 |
| Brotli Q11 | 0.46 | 0.01 | 77.03x | 0 | 680 | PASS | 2.1 |
| gzip -6 | 0.46 | 0.03 | 15.35x | 118 | 388 | PASS | 2.5 |
| gzip -9 | 0.46 | 0.03 | 15.72x | 74 | 369 | PASS | 2.9 |

## PostgreSQL slow query

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 0.68 | 0.01 | 61.49x | 1 | 23 | PASS | 82.0 |
| Zstd L3 | 0.68 | 0.03 | 19.98x | 493 | 1419 | PASS | 2.2 |
| Zstd L9 | 0.68 | 0.03 | 20.11x | 64 | 1305 | PASS | 2.1 |
| Zstd L19 | 0.68 | 0.02 | 28.02x | 1 | 1252 | PASS | 2.1 |
| Zstd L22 | 0.68 | 0.02 | 27.85x | 1 | 1292 | PASS | 2.1 |
| LZ4 | 0.68 | 0.12 | 5.88x | 1110 | 1306 | PASS | 2.1 |
| Brotli Q5 | 0.68 | 0.02 | 30.17x | 94 | 662 | PASS | 2.7 |
| Brotli Q9 | 0.68 | 0.02 | 32.21x | 29 | 631 | PASS | 2.8 |
| Brotli Q11 | 0.68 | 0.01 | 46.63x | 1 | 663 | PASS | 2.6 |
| gzip -6 | 0.68 | 0.06 | 11.51x | 118 | 390 | PASS | 3.2 |
| gzip -9 | 0.68 | 0.06 | 11.63x | 72 | 462 | PASS | 3.2 |
