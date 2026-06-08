#!/usr/bin/env python3
"""
NULL_Orchestrator - [NULL MASTER v1]
====================================
MISSION: Unified entry point for all NULL Engines.
FEAT:    Automatic Type Detection + Safety Valve Integration.
"""

import sys
import os
import json
import re
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

        # Security Layer — constructed lazily so the orchestrator can be created
        # without a secret (e.g. to inspect engines). The encrypting compress/
        # decompress paths call _require_security(), which raises if no explicit
        # secret was provided rather than falling back to a public default key.
        self._security_secret = security_secret
        self._security = None

        # Engine registry: key -> (module_name, class_name, protocol_id)
        # IMPORTANT: every protocol_id must be unique — duplicate IDs cause wrong
        # champion selection during decompress (last-write wins in registry dict).
        self.engines = {
            # JSON / structured
            'json_columnar':     ('NULL_Json_Columnar_Gun_v1',          'NULL_Json_Columnar_Gun_v1',          b'COL2'),
            'json_entropy':      ('NULL_Json_Entropy_Focused',           'NULL_Json_Entropy_Focused',           b'JEN1'),
            'json_repetitive':   ('NULL_Json_Repetition_Focused',        'NULL_Json_Repetition_Focused',        b'JRP1'),
            # Nginx
            'nginx_entropy':     ('NULL_Nginx_Entropy_Focused',          'NULL_Nginx_Entropy_Focused',          b'NGX1'),
            'nginx_repetitive':  ('NULL_Nginx_Repetition_Focused',       'NULL_Nginx_Repetition_Focused',       b'NGX2'),
            # Apache
            'apache_entropy':    ('NULL_Apache_Entropy_Focused',         'NULL_Apache_Entropy_Focused',         b'APH1'),
            'apache_repetitive': ('NULL_Apache_Repetition_Focused',      'NULL_Apache_Repetition_Focused',      b'APH2'),
            # Syslog
            'syslog_entropy':    ('NULL_Syslog_Entropy_Focused',         'NULL_Syslog_Entropy_Focused',         b'SLG1'),
            'syslog_repetitive': ('NULL_Syslog_Repetition_Focused',      'NULL_Syslog_Repetition_Focused',      b'SLG2'),
            # K8s
            'k8s_entropy':       ('NULL_K8s_Entropy_Focused',            'NULL_K8s_Entropy_Focused',            b'K8S1'),
            'k8s_velocity':      ('NULL_K8s_Native_Velocity',            'NULL_K8s_Native_Velocity',            b'K8S2'),
            # SQL / Postgres
            'sql_entropy':       ('NULL_Sql_Entropy_Focused',            'NULL_Sql_Entropy_Focused',            b'SQL1'),
            'sql_repetitive':    ('NULL_Sql_Repetition_Focused',         'NULL_Sql_Repetition_Focused',         b'SQL2'),
            'sql_velocity':      ('NULL_Sql_Native_Velocity',            'NULL_Sql_Native_Velocity',            b'SQL3'),
            # AWS
            'cloudtrail':        ('NULL_Aws_CloudTrail_Entropy_Focused', 'NULL_Aws_CloudTrail_Entropy_Focused', b'CTL1'),
            'vpcflow':           ('NULL_Aws_VpcFlow_Entropy_Focused',    'NULL_Aws_VpcFlow_Entropy_Focused',    b'VPC1'),
            # Other
            'netflow':           ('NULL_Netflow_V5_Entropy_Focused',     'NULL_Netflow_V5_Entropy_Focused',     b'NFW1'),
            'vmware':            ('NULL_Vmware_Entropy_Focused',         'NULL_Vmware_Entropy_Focused',         b'VMW1'),
            'windows_evtx':      ('NULL_Windows_Evtx_Entropy_Focused',   'NULL_Windows_Evtx_Entropy_Focused',   b'EVT1'),
            'github_scm':        ('NULL_Scm_GitHub_Entropy_Focused',     'NULL_Scm_GitHub_Entropy_Focused',     b'SCM1'),
            # Universal fallback
            'universal_entropy': ('NULL_Universal_Entropy_Focused',      'NULL_Universal_Entropy_Focused',      b'UNV1'),
            'universal_rep':     ('NULL_Universal_Repetition_Focused',   'NULL_Universal_Repetition_Focused',   b'UNV2'),
        }
        self.registry = {}  # protocol_id -> decompress_func

    def _require_security(self) -> "NULL_Security_Layer":
        """Lazily build the security layer for the encrypting paths.

        Raises ValueError (from NULL_Security_Layer) if no explicit secret was
        provided — we never silently encrypt with a public default key.
        """
        if self._security is None:
            self._security = NULL_Security_Layer(master_secret=self._security_secret)
        return self._security

    # ── Format auto-detection ────────────────────────────────────────────────

    _IP_RE  = re.compile(rb'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    _SYS_RE = re.compile(rb'^[A-Z][a-z]{2}\s+\d')
    _K8S_KW = {b'"stream"', b'"pod"', b'"namespace"', b'"container"'}
    _SQL_KW = {b'"duration_ms"', b'"query"', b'SELECT ', b'INSERT ', b'UPDATE '}
    _AWS_KW = {b'"eventName"', b'"awsRegion"', b'"userAgent"', b'"eventVersion"'}
    _VPC_KW = {b'"srcAddr"', b'"dstAddr"', b'"srcPort"'}

    def detect_engine(self, data: bytes) -> str:
        """Sniff 4KB sample and return the best engine key."""
        sample = data[:4096]
        lines  = [l.strip() for l in sample.splitlines() if l.strip()]
        if not lines:
            return 'universal_entropy'
        first = lines[0]

        # AWS CloudTrail / VPC Flow (check before generic JSON)
        if any(kw in sample for kw in self._AWS_KW):
            return 'cloudtrail'
        if any(kw in sample for kw in self._VPC_KW):
            return 'vpcflow'

        # K8s JSON
        if any(kw in sample for kw in self._K8S_KW):
            return 'k8s_entropy'

        # SQL / Postgres
        if any(kw in sample for kw in self._SQL_KW):
            return 'sql_entropy'

        # Generic JSON (try parse first line)
        try:
            obj = json.loads(first)
            if isinstance(obj, dict):
                return 'json_columnar'
        except Exception:
            pass

        # Nginx / Apache access logs (start with IP)
        if self._IP_RE.match(first):
            return 'nginx_entropy' if b'"nginx' in sample or b'nginx' in sample.lower() else 'apache_entropy'

        # Syslog (RFC 3164: "Jan  1 00:00:00 hostname proc[pid]: msg")
        if self._SYS_RE.match(first):
            return 'syslog_entropy'

        # GitHub SCM
        if b'"repo"' in sample and b'"actor"' in sample:
            return 'github_scm'

        return 'universal_entropy'

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

    def compress(self, data: bytes, engine_key: str = None, tenant_id: str = "default") -> bytes:
        """
        Full Pipeline:
        1. Auto-detect format (if engine_key is None)
        2. Safe Seal (Compression + MRTV Verification)
        3. Secure Seal (Encryption + Tenant Isolation + Audit Trail)
        """
        import time
        start_time = time.time()

        if engine_key is None:
            engine_key = self.detect_engine(data)

        engine, proto_id = self._get_engine(engine_key)

        # 1. Compress + Verify (Safety Valve)
        compressed_blob = Valve.seal(data, engine.compress, engine.decompress, proto_id[:4].ljust(4, b'\x00'))

        # 2. Encrypt + Isolate (Security Layer)
        secure_blob = self._require_security().seal(compressed_blob, tenant_id, {
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
        compressed_blob, audit_meta = self._require_security().unseal(secure_blob, tenant_id)

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

