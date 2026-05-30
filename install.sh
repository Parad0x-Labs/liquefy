#!/bin/bash
# --- $NULL SOVEREIGN SDK INSTALLER ---
# This script prepares your environment for offline .null recovery.

echo "--- Parad0x Labs: Sovereign SDK Setup ---"

# Check for Docker
if ! [ -x "$(command -v docker)" ]; then
  echo "[-] Error: Docker is not installed. This SDK requires Docker for the hardened conduction environment."
  exit 1
fi

echo "[+] Pulling Hardened $NULL Appliance..."
docker pull nullaai/liquefy-decoder-public@sha256:b7a0499f38d192e7333c760fcf8e429abcff83e58610259841f2ffb525c02935

echo "[+] Setting up 'liquefy' CLI command..."
chmod +x ./liquefy
echo "[+] Done. Run: ./liquefy version"

echo "[!] SDK Ready. You can now use './liquefy decompress <file.null>' for data recovery."

