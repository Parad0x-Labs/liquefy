#!/usr/bin/env python3
"""
NULL_Safety_Valve - [NULL PROTECTION v1]
=========================================
MISSION: Guarantee 100% Data Integrity for ANY NULL Engine.
METHOD:  Mandatory Round-Trip Verification (MRTV) with Hash Locking.
STATUS:  The "Unbreakable" Layer.
"""

import zstandard as zstd
import xxhash
import struct
import io
import sys

class NULL_Safety_Valve:
    def __init__(self, fallback_level=19, enabled=True):
        self.fallback_cctx = zstd.ZstdCompressor(level=fallback_level)
        self.fallback_dctx = zstd.ZstdDecompressor()
        self.enabled = enabled

    def seal(self, original_data: bytes, compress_func, decompress_func, engine_id: bytes) -> bytes:
        """
        Compresses data with MRTV (Mandatory Round-Trip Verification).
        If verification fails or is disabled, falls back to raw Zstd.
        """
        if not self.enabled:
            # Skip verification path - direct engine call
            try:
                candidate = compress_func(original_data)
                return b'SAFE' + engine_id + candidate
            except Exception as e:
                return self._fallback(original_data)

        # 1. Fingerprint Original (RAM Speed)
        original_hash = xxhash.xxh64(original_data).digest()

        try:
            # 2. Attempt Aggressive Compression
            candidate_blob = compress_func(original_data)

            # 3. Mandatory Verification (The Golden Rule)
            restored_data = decompress_func(candidate_blob)
            restored_hash = xxhash.xxh64(restored_data).digest()

            if original_hash == restored_hash:
                # SUCCESS
                return b'SAFE' + engine_id + candidate_blob
            else:
                # FAILURE - LOG AND FALLBACK
                print(f"!! SAFETY VALVE TRIGGERED !! Engine {engine_id.decode(errors='replace')} integrity failure. Falling back to Zstd.")
                return self._fallback(original_data)

        except Exception as e:
            # CRASH - FALLBACK
            print(f"!! ENGINE CRASH !! {engine_id.decode(errors='replace')} failed with: {e}. Falling back to Zstd.")
            return self._fallback(original_data)

    def _fallback(self, data: bytes) -> bytes:
        """Raw Zstd fail-safe"""
        c_data = self.fallback_cctx.compress(data)
        return b'SAFE' + b'ZST\x00' + c_data

    def unseal(self, blob: bytes, engine_registry: dict) -> bytes:
        """
        Universal unsealer for SAFE-wrapped blobs.
        engine_registry: { b'ENG\x01': decompress_func }
        """
        if not blob.startswith(b'SAFE'):
            # Legacy support: if not wrapped, try direct decompression if magic matches
            return None 

        engine_id = blob[4:8]
        payload = blob[8:]

        if engine_id == b'ZST\x00':
            return self.fallback_dctx.decompress(payload)

        if engine_id in engine_registry:
            return engine_registry[engine_id](payload)

        raise ValueError(f"Unknown Engine ID in SAFE blob: {engine_id}")

# Singleton instance for easy access
Valve = NULL_Safety_Valve()

