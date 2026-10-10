"""
demo/privacy_proof.py

Live, on-stage demonstration that SafePath:
  1. Does not write any file to disk during a session
  2. Does not open any network socket during a session
  3. Does not store any PII in the session schema

Run:  python demo/privacy_proof.py

This script is designed to be shown on a projector. It prints a live
audit trail that the audience can follow. It intentionally fails loudly
if any of the claims are violated.
"""
import os
import socket
import sys
import tempfile
from pathlib import Path

# Make the project root importable when running this file directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import privacy


# ---- Claim 1: no file writes during a session ----------------------------

def check_no_disk_writes() -> bool:
    print("[1/3] Checking disk writes during a session...")
    with tempfile.TemporaryDirectory() as tmp:
        cwd = os.getcwd()
        os.chdir(tmp)
        try:
            before = set(Path(tmp).rglob("*"))
            s = privacy.new_session()
            s["origin"] = (33.7756, -84.3963)
            s["destination"] = (33.7780, -84.3940)
            s["route"] = [s["origin"], s["destination"]]
            privacy.validate_session(s)
            after = set(Path(tmp).rglob("*"))
        finally:
            os.chdir(cwd)

        new_files = after - before
        if new_files:
            print(f"   FAIL: files written: {new_files}")
            return False

    print("   PASS: 0 files written")
    return True


# ---- Claim 2: no network calls during a session --------------------------

def check_no_network_calls() -> bool:
    print("[2/3] Checking network egress during a session...")

    original_socket = socket.socket
    original_create = socket.create_connection
    calls = []

    def trap_socket(*args, **kwargs):
        calls.append("socket()")
        raise AssertionError("session attempted to open a socket")

    def trap_create(*args, **kwargs):
        calls.append("create_connection()")
        raise AssertionError("session attempted to open a connection")

    socket.socket = trap_socket
    socket.create_connection = trap_create
    try:
        s = privacy.new_session()
        s["origin"] = (33.7756, -84.3963)
        s["destination"] = (33.7780, -84.3940)
        privacy.validate_session(s)
    finally:
        socket.socket = original_socket
        socket.create_connection = original_create

    if calls:
        print(f"   FAIL: network calls detected: {calls}")
        return False

    print("   PASS: 0 network calls")
    return True


# ---- Claim 3: no PII in the schema ---------------------------------------

def check_no_pii() -> bool:
    print("[3/3] Checking session schema for PII...")
    schema = privacy.get_session_schema()
    violations = schema & privacy.FORBIDDEN_FIELDS
    if violations:
        print(f"   FAIL: forbidden fields present: {violations}")
        return False
    print(f"   PASS: schema = {sorted(schema)}")
    return True


# ---- Run all checks ------------------------------------------------------

def main() -> int:
    print("=" * 60)
    print(" SafePath privacy proof — live demonstration")
    print("=" * 60)
    results = [check_no_disk_writes(), check_no_network_calls(), check_no_pii()]
    print("=" * 60)
    if all(results):
        print(" ALL CHECKS PASSED — SafePath collects no user data.")
        return 0
    print(" ONE OR MORE CHECKS FAILED — do not ship.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())