#!/usr/bin/env python3
"""
LIQUEFY UNICORN: END-TO-END (E2E) VERIFICATION
==============================================
Tests the full pipeline from Data -> Orchestrator -> Disk -> Rust Search -> Result.
"""

import sys
import os
import json
import time
import subprocess
from pathlib import Path

# Setup Paths
BASE_DIR = Path(__file__).parent.resolve()
sys.path.append(str(BASE_DIR.parent / "api"))
sys.path.append(str(BASE_DIR / "unicorn_engines" / "json_codec"))

try:
    from hyper_orchestrator import HyperOrchestrator
except ImportError:
    print("CRITICAL: Engines not found.")
    sys.exit(1)

def print_step(step, msg):
    print(f"\n[STEP {step}] {msg}")
    time.sleep(0.5)

def run_e2e():
    print("=== LIQUEFY UNICORN E2E SELF-TEST ===")
    
    # STEP 1: Generate Gold Master Data
    print_step(1, "Generating 'Gold Master' Data...")
    test_file = BASE_DIR / "e2e_test.jsonl"
    target_query = "CRITICAL_FAILURE_X99"
    
    logs = []
    # 10,000 lines of noise
    for i in range(10000):
        logs.append(json.dumps({"ts": i, "level": "INFO", "msg": "routine check"}))
    
    # 5 lines of Gold
    for i in range(5):
        # Make the gold lines distinct so COL2 dictionary doesn't just eat them perfectly?
        # No, we want structure.
        logs.append(json.dumps({"ts": 10000+i, "level": "ERROR", "msg": f"{target_query} detected"}))
        
    data = "\n".join(logs).encode('utf-8')
    
    # FORCE AUDITION BYPASS FOR TEST
    # We want to test the PIPELINE, not just the Orchestrator's opinion on 500KB files.
    # The E2E test fails if Orchestrator chooses Zstd, because then we don't test Rust Search.
    
    # But wait, we can't change orchestrator code from here easily.
    # We can just make the data bigger? 
    # Or we can accept that for this test script, we call the engine directly?
    # NO, the user said "try to do e2e yourself". Orchestrator is part of E2E.
    
    # Let's generate MORE data to pass the small file threshold (1MB).
    # 10,000 lines was 500KB. Let's do 30,000 lines.
    
    logs = []
    for i in range(30000):
        logs.append(json.dumps({"ts": i, "level": "INFO", "msg": "routine check"}))
    for i in range(5):
        logs.append(json.dumps({"ts": 30000+i, "level": "ERROR", "msg": f"{target_query} detected"}))
    data = "\n".join(logs).encode('utf-8')
    
    with open(test_file, "wb") as f:
        f.write(data)
        
    print(f"   -> Generated {len(logs)} lines ({len(data)/1024:.2f} KB).")
    print(f"   -> Target matches: 5")

    # STEP 2: Hyper-Orchestrator Ingest
    print_step(2, "Running Hyper-Orchestrator (Compression)...")
    orch = HyperOrchestrator()
    start = time.time()
    compressed_blob, engine = orch.compress(data)
    duration = (time.time() - start) * 1000
    
    output_file = test_file.with_suffix(".col2")
    with open(output_file, "wb") as f:
        f.write(compressed_blob)
        
    print(f"   -> Engine Selected: {engine}")
    print(f"   -> Compressed Size: {len(compressed_blob)/1024:.2f} KB")
    print(f"   -> Time: {duration:.2f} ms")
    
    if engine != 'LIQUEFY_COL2':
        print("   !!! FAILURE: Orchestrator chose wrong engine for clean JSON!")
        sys.exit(1)

    # STEP 3: Rust Core Search
    print_step(3, "Executing Rust Core Search (via WSL)...")
    
    # Path translation for WSL
    wsl_bin = "/mnt/f/Enterprise\\ \\ tests/research/rust_core/target/release/liquefy-core"
    
    # Escape spaces in Windows path for WSL usage
    # relative_to logic might be brittle if drive letters differ, hardcoding relative path for safety
    # We are in f:\Enterprise tests\research
    wsl_file = "/mnt/f/Enterprise\\ \\ tests/research/e2e_test.col2"
    
    cmd = ["wsl", "--exec", "bash", "-c", f"{wsl_bin} {wsl_file} '{target_query}'"]
    
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    rust_duration = (time.time() - start) * 1000
    
    if result.returncode != 0:
        print(f"   !!! RUST ERROR: {result.stderr}")
        sys.exit(1)
        
    try:
        stats = json.loads(result.stdout)
        print(f"   -> Rust Output: {json.dumps(stats, indent=2)}")
    except json.JSONDecodeError:
        print(f"   !!! INVALID JSON FROM RUST: {result.stdout}")
        sys.exit(1)

    # STEP 4: Verification
    print_step(4, "Verifying Results...")
    
    found = stats.get("found", -1)
    if found == 5:
        print("   -> MATCH CONFIRMED: Found exactly 5 records.")
    else:
        print(f"   !!! MISMATCH: Expected 5, found {found}")
        sys.exit(1)
        
    # STEP 5: Integrity Check (Decompression)
    print_step(5, "Verifying Bit-Perfect Restore...")
    restored = orch.col_engine.decompress(compressed_blob)
    
    if restored == data:
        print("   -> SHA256 MATCH: Restored data is identical to input.")
    else:
        print("   !!! DATA CORRUPTION DETECTED !!!")
        sys.exit(1)

    print("\n=== E2E TEST PASSED: UNICORN IS REAL ===")
    
    # Cleanup
    try:
        os.remove(test_file)
        os.remove(output_file)
    except: pass

if __name__ == "__main__":
    run_e2e()
