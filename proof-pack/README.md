# $NULL Sovereign Proof Pack (v3.5)

This pack contains reference samples and cryptographic proofs to validate the Liquefy Conduction Engine on your local machine.

## Directory Structure
- `/samples/raw/`: Original uncompressed telemetry samples (illustrative).
- `/samples/compressed/`: Production-grade `.null` archives.
- `/samples/restored/`: Bit-perfect restorations produced by the public SDK.
- `hashes.txt`: SHA-256 integrity map for all samples.

## Verification Command
```bash
./liquefy verify proof-pack/samples/compressed/sample_syslog.null
```

## Decompression Proof
```bash
./liquefy decompress proof-pack/samples/compressed/sample_syslog.null restored.log
diff proof-pack/samples/raw/sample_syslog.log restored.log
```

---
© 2026 Parad0x Labs. 🚀
