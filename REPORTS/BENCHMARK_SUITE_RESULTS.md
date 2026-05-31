# Liquefy Benchmark Suite Results

Generated against 5,000 lines per dataset.

Search latency = time to find a target string in the compressed archive.

Liquefy uses native columnar grep (no full decompress). All others decompress then scan.

---

## JSON agent logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 0.75 | 0.01 | 136.92x | 1 | 18 | PASS | - |
| Zstd L3 | 0.75 | 0.02 | 37.69x | 378 | 768 | PASS | - |
| Zstd L9 | 0.75 | 0.02 | 36.35x | 36 | 718 | PASS | - |
| Zstd L19 | 0.75 | 0.02 | 46.50x | 2 | 361 | PASS | - |
| Zstd L22 | 0.75 | 0.02 | 46.50x | 1 | 1285 | PASS | - |
| LZ4 | 0.75 | 0.11 | 7.14x | 619 | 1293 | PASS | - |
| Brotli Q5 | 0.75 | 0.02 | 45.38x | 57 | 368 | PASS | - |
| Brotli Q9 | 0.75 | 0.01 | 55.44x | 31 | 653 | PASS | - |
| Brotli Q11 | 0.75 | 0.01 | 58.85x | 1 | 557 | PASS | - |
| gzip -6 | 0.75 | 0.06 | 13.16x | 106 | 210 | PASS | - |
| gzip -9 | 0.75 | 0.06 | 13.41x | 52 | 386 | PASS | - |

## Payment receipts

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 0.60 | 0.00 | 357.09x | 6 | 12 | PASS | - |
| Zstd L3 | 0.60 | 0.01 | 40.47x | 293 | 793 | PASS | - |
| Zstd L9 | 0.60 | 0.01 | 49.77x | 72 | 1272 | PASS | - |
| Zstd L19 | 0.60 | 0.02 | 40.19x | 1 | 916 | PASS | - |
| Zstd L22 | 0.60 | 0.02 | 39.72x | 1 | 1088 | PASS | - |
| LZ4 | 0.60 | 0.09 | 6.81x | 1396 | 1023 | PASS | - |
| Brotli Q5 | 0.60 | 0.01 | 44.42x | 88 | 464 | PASS | - |
| Brotli Q9 | 0.60 | 0.01 | 45.59x | 24 | 520 | PASS | - |
| Brotli Q11 | 0.60 | 0.01 | 49.21x | 0 | 458 | PASS | - |
| gzip -6 | 0.60 | 0.04 | 13.92x | 120 | 412 | PASS | - |
| gzip -9 | 0.60 | 0.04 | 14.23x | 69 | 348 | PASS | - |

## Nginx access logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.46 | 0.05 | 9.30x | 299 | 560 | PASS | - |
| Zstd L9 | 0.46 | 0.04 | 12.89x | 46 | 853 | PASS | - |
| Zstd L19 | 0.46 | 0.03 | 16.67x | 1 | 1061 | PASS | - |
| Zstd L22 | 0.46 | 0.03 | 16.67x | 1 | 1071 | PASS | - |
| LZ4 | 0.46 | 0.09 | 5.31x | 1077 | 1012 | PASS | - |
| Brotli Q5 | 0.46 | 0.03 | 15.65x | 65 | 329 | PASS | - |
| Brotli Q9 | 0.46 | 0.02 | 27.78x | 22 | 434 | PASS | - |
| Brotli Q11 | 0.46 | 0.02 | 30.66x | 0 | 525 | PASS | - |
| gzip -6 | 0.46 | 0.04 | 11.33x | 62 | 288 | PASS | - |
| gzip -9 | 0.46 | 0.04 | 11.71x | 58 | 382 | PASS | - |

## Kubernetes logs

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 0.76 | 0.00 | 475.81x | 10 | 25 | PASS | - |
| Zstd L3 | 0.76 | 0.00 | 175.71x | 1692 | 2640 | PASS | - |
| Zstd L9 | 0.76 | 0.00 | 314.20x | 154 | 1280 | PASS | - |
| Zstd L19 | 0.76 | 0.00 | 370.92x | 5 | 917 | PASS | - |
| Zstd L22 | 0.76 | 0.00 | 370.92x | 5 | 1732 | PASS | - |
| LZ4 | 0.76 | 0.04 | 18.05x | 2317 | 852 | PASS | - |
| Brotli Q5 | 0.76 | 0.00 | 481.52x | 187 | 374 | PASS | - |
| Brotli Q9 | 0.76 | 0.00 | 515.38x | 89 | 544 | PASS | - |
| Brotli Q11 | 0.76 | 0.00 | 599.25x | 2 | 183 | PASS | - |
| gzip -6 | 0.76 | 0.02 | 33.43x | 89 | 256 | PASS | - |
| gzip -9 | 0.76 | 0.02 | 48.58x | 54 | 170 | PASS | - |

## Syslog (RFC 3164)

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zstd L3 | 0.46 | 0.02 | 29.28x | 368 | 840 | PASS | - |
| Zstd L9 | 0.46 | 0.01 | 42.47x | 41 | 548 | PASS | - |
| Zstd L19 | 0.46 | 0.01 | 41.28x | 1 | 992 | PASS | - |
| Zstd L22 | 0.46 | 0.01 | 41.28x | 1 | 956 | PASS | - |
| LZ4 | 0.46 | 0.08 | 5.75x | 597 | 385 | PASS | - |
| Brotli Q5 | 0.46 | 0.01 | 50.42x | 48 | 836 | PASS | - |
| Brotli Q9 | 0.46 | 0.01 | 53.84x | 19 | 369 | PASS | - |
| Brotli Q11 | 0.46 | 0.01 | 77.03x | 0 | 206 | PASS | - |
| gzip -6 | 0.46 | 0.03 | 15.35x | 84 | 233 | PASS | - |
| gzip -9 | 0.46 | 0.03 | 15.72x | 74 | 345 | PASS | - |

## PostgreSQL slow query

| Compressor | Raw MB | Comp MB | Ratio | Comp MB/s | Decomp MB/s | BitPerfect | Search ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Liquefy COL | 0.68 | 0.01 | 70.42x | 1 | 18 | PASS | - |
| Zstd L3 | 0.68 | 0.03 | 19.98x | 604 | 1229 | PASS | - |
| Zstd L9 | 0.68 | 0.03 | 20.11x | 58 | 1656 | PASS | - |
| Zstd L19 | 0.68 | 0.02 | 28.02x | 1 | 1181 | PASS | - |
| Zstd L22 | 0.68 | 0.02 | 27.85x | 1 | 1212 | PASS | - |
| LZ4 | 0.68 | 0.12 | 5.88x | 934 | 1141 | PASS | - |
| Brotli Q5 | 0.68 | 0.02 | 30.17x | 90 | 582 | PASS | - |
| Brotli Q9 | 0.68 | 0.02 | 32.21x | 28 | 682 | PASS | - |
| Brotli Q11 | 0.68 | 0.01 | 46.63x | 0 | 697 | PASS | - |
| gzip -6 | 0.68 | 0.06 | 11.51x | 119 | 428 | PASS | - |
| gzip -9 | 0.68 | 0.06 | 11.63x | 68 | 385 | PASS | - |
