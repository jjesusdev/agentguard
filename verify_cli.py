"""Verify command."""
import sys
from pathlib import Path
from agentguard.verify import verify_journal

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: verify <session_id>")
        sys.exit(1)
    session_id = sys.argv[1]
    ok, bad = verify_journal(session_id, Path("var/lib/agentguard/sessions"))
    if ok:
        print(f"OK: journal {session_id} verified")
    else:
        print(f"TAMPERED at seq {bad}")
