#!/usr/bin/env python3
"""
NULL_Orchestrator - [NULL MASTER v1]
====================================
MISSION: Unified entry point for all NULL Engines.
FEAT:    Automatic Type Detection + Safety Valve Integration.
"""

import sys
import os
from pathlib import Path

# Add all subdirectories to sys.path
BASE_DIR = Path(__file__).parent
for d in BASE_DIR.iterdir():
    if d.is_dir(): sys.path.insert(0, str(d))

from safety_valve import Valve
from security_compliance import NULL_Security_Layer, secure_audit_log
from observability import Vision

class NULLA:
    """NULL AI Agent - Enterprise Deployment Specialist"""
    def speak(self, message: str) -> str:
        """Return formatted message with NULLA branding"""
        return f"[NULLA AGENT] {message}"

class NULL_Orchestrator:
    def __init__(self, safety_enabled=None, security_secret=None):
        # Default to True, but check environment variable for easy toggle
        if safety_enabled is None:
            safety_enabled = os.environ.get("NULL_SAFETY_OFF", "0") != "1"
            
        self.safety_enabled = safety_enabled
        Valve.enabled = safety_enabled
        
        # Security Layer
        self.security = NULL_Security_Layer(master_secret=security_secret)
        
        # Load all engines (Lazy loading recommended for production)
        # For this v1, we map IDs to modules
        self.engines = {
            # 'ID' : (Module, Name, ProtocolID)
            'apache_entropy': ('NULL_Apache_Entropy_Focused', 'NULL_Apache_Entropy_Focused', b'LPRM'),
            'apache_repetitive': ('NULL_Apache_Repetition_Focused', 'NULL_Apache_Repetition_Focused', b'UNI\x01'),
            'universal_entropy': ('NULL_Universal_Entropy_Focused', 'NULL_Universal_Entropy_Focused', b'NMX5'),
            'cloudtrail': ('NULL_Aws_CloudTrail_Entropy_Focused', 'NULL_Aws_CloudTrail_Entropy_Focused', b'CTL\x01'),
            'json_columnar': ('NULL_Json_Columnar_Gun_v1', 'NULL_Json_Columnar_Gun_v1', b'COL1'),
            'json_entropy': ('NULL_Json_Entropy_Focused', 'NULL_Json_Entropy_Focused', b'COL1'),
            # ... and so on for all 21 champions
        }
        self.registry = {} # ID -> Decompress Func

    def get_nulla(self):
        """Get the NULL AI agent for deployment coordination"""
        return NULLA()

    def _get_engine(self, engine_key):
        mod_name, class_name, proto_id = self.engines[engine_key]
        mod = __import__(mod_name)
        engine_class = getattr(mod, class_name)
        engine = engine_class()
        self.registry[proto_id] = engine.decompress
        return engine, proto_id

    def compress(self, data: bytes, engine_key: str, tenant_id: str = "default") -> bytes:
        """
        Full Pipeline:
        1. Select Engine
        2. Safe Seal (Compression + MRTV Verification)
        3. Secure Seal (Encryption + Tenant Isolation + Audit Trail)
        """
        import time
        start_time = time.time()

        engine, proto_id = self._get_engine(engine_key)

        # 1. Compress + Verify (Safety Valve)
        compressed_blob = Valve.seal(data, engine.compress, engine.decompress, proto_id[:4].ljust(4, b'\x00'))

        # 2. Encrypt + Isolate (Security Layer)
        secure_blob = self.security.seal(compressed_blob, tenant_id, {
            "engine": engine_key,
            "original_size": len(data),
            "safety": self.safety_enabled
        })

        # 3. Track metrics (Observability)
        duration_ms = (time.time() - start_time) * 1000
        Vision.track_op(engine_key, tenant_id, len(data), len(secure_blob), duration_ms, True)

        secure_audit_log("COMPRESS_EVENT", {"tenant": tenant_id, "engine": engine_key})
        return secure_blob

    def decompress(self, secure_blob: bytes, tenant_id: str = "default") -> bytes:
        """
        Reverse Pipeline:
        1. Verify Identity & Decrypt (Security Layer)
        2. Validate & Decompress (Safety Valve)
        """
        import time
        start_time = time.time()

        # 1. Auth & Decrypt
        compressed_blob, audit_meta = self.security.unseal(secure_blob, tenant_id)

        # 2. Decompress
        if not self.registry:
            for k in self.engines.keys():
                self._get_engine(k)

        data = Valve.unseal(compressed_blob, self.registry)

        # 3. Track metrics (Observability)
        duration_ms = (time.time() - start_time) * 1000
        Vision.track_op(audit_meta.get("engine", "unknown"), tenant_id, audit_meta.get("original_size", 0), len(secure_blob), duration_ms, True)

        secure_audit_log("DECOMPRESS_EVENT", {"tenant": tenant_id, "meta": audit_meta})
        return data

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python NULL_Orchestrator_v1.py [compress|decompress] <engine_key> <file>")
        print("Engines: apache_entropy, apache_repetitive, universal_entropy, cloudtrail...")
        sys.exit(1)

    cmd, engine_key, file_path = sys.argv[1], sys.argv[2], sys.argv[3]
    orch = NULL_Orchestrator(safety_enabled=True)
    
    with open(file_path, "rb") as f: data = f.read()
    
    if cmd == "compress":
        out = orch.compress(data, engine_key)
        with open(file_path + ".null", "wb") as f: f.write(out)
        print(f"Compressed with {engine_key}. Safety: {orch.safety_enabled}")
    elif cmd == "decompress":
        out = orch.decompress(data)
        with open(file_path + ".orig", "wb") as f: f.write(out)
        print(f"Decompressed. Safety checked.")

