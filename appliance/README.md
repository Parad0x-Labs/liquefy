# Liquefy Sealed Decoder Appliance

This directory contains the specification and build harness for the Liquefy Sealed Decoder Appliance.

## Overview

The appliance is a "Blackbox" container designed for maximum security and IP protection. It allows enterprise customers to decompress and verify archives locally while ensuring the proprietary compression kernels remain protected.

## Security Features

1. **Distroless Base:** No shell, no package manager, no unnecessary binaries.
2. **Network Isolation:** Designed to run with `--network=none`.
3. **Hardened Runtime:** Supports read-only root filesystems and capability dropping.
4. **Non-Root Execution:** Runs as a dedicated non-privileged user.

## Build Instructions (For Internal Build Pipelines)

The `Dockerfile` here is the public specification. The `liquefy-decoder` binary is injected during the private CI/CD process.

```bash
# Example build command (Internal)
docker build -t parad0xlabs/liquefy-decoder:latest .
```

## Usage

See [docs/enterprise-evaluation.md](../docs/enterprise-evaluation.md) for detailed usage instructions.

