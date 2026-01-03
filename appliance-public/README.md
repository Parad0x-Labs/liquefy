# Liquefy Public Decode-Only Appliance

## Version: v3.7-Quantum-Omni-Engine (Public)

This appliance provides **decode-only access** to Liquefy production archives.

### Key Features
- **Identity-Aware Handshake:** Automatically detects and verifies tenant identities for cryptographic unsealing.
- **Quantum Stream Restoration:** Scans and reassembles concatenated conduction frames for "Tailed" or "Appended" logs.
- **Omni-Engine Reconstruction:** Full reassembly logic for all 23 conduction engines (SYSL, JSC, HYP, SQL, K8S, etc.).
- **Hardened Execution:** Runs in a network-isolated, read-only, non-root container environment.

## Capabilities
- Decompress `.null` / `.liq` archives
- Verify integrity (SHA256)
- Fully offline
- No license required

## Explicit Limitations
- Cannot compress
- Cannot create archives
- Cannot tune engines
- Cannot access orchestration logic
- No performance guarantees

This appliance exists solely to ensure data recoverability and trust.

