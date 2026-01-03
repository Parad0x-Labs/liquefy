# STAGE 1: The Build Vault
FROM python:3.9-slim AS builder

RUN apt-get update && apt-get install -y binutils && rm -rf /var/lib/apt/lists/*
RUN pip install pyinstaller zstandard xxhash cryptography

WORKDIR /build
COPY decoder_source.py .

# Compile Python into a single, stripped binary
RUN pyinstaller --onefile --name liquefy-decoder-public decoder_source.py

# STAGE 2: The Hardened Appliance (Professional Base)
FROM python:3.9-slim

# Install minimal runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends libstdc++6 && rm -rf /var/lib/apt/lists/*

# Create a non-root user for secure conduction
RUN groupadd -r parad0x && useradd -r -g parad0x nulla
USER nulla

WORKDIR /data

# Copy only the compiled binary and the entrypoint
COPY --from=builder /build/dist/liquefy-decoder-public /usr/local/bin/liquefy-decoder-public
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Ensure execute permissions (as root)
USER root
RUN chmod +x /usr/local/bin/entrypoint.sh /usr/local/bin/liquefy-decoder-public
USER nulla

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
