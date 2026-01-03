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
# Placeholder for the public image
# docker pull parad0xlabs/liquefy-decoder-public:latest

echo "[+] Setting up 'liquefy' CLI command..."
chmod +x ./liquefy

echo "[!] SDK Ready. You can now use './liquefy decompress <file.null>' for data recovery."

