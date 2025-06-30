# This is required in case database is in correct state but migrations are out of sync locally.
# Usage: recursively applies migration, if it sees migration is already applied mark fake on it.
# This is much better than destroying db and restarting it.

import os
import re
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MANAGE_PY = BASE_DIR / "manage.py"

DUPLICATE_PATTERNS = (
    re.compile(r"already exists", re.IGNORECASE),
    re.compile(r"duplicate column", re.IGNORECASE),
    re.compile(r"duplicate table", re.IGNORECASE),
)

APPLY_PATTERN = re.compile(r"Applying (\w+)\.(\w+)")


def run_manage(*cmd: str) -> tuple[int, str]:
    """Run a manage.py command and return (exit_code, combined_output)."""
    process = subprocess.run(
        [sys.executable, str(MANAGE_PY), *cmd],
        text=True,
        capture_output=True,
        env=os.environ,
    )
    output = process.stdout + process.stderr
    return process.returncode, output


def has_duplicate_error(output: str) -> bool:
    return any(p.search(output) for p in DUPLICATE_PATTERNS)


def extract_offending_migration(output: str) -> tuple[str, str] | None:
    """Return (app, migration_name) if found in output."""
    match = APPLY_PATTERN.search(output)
    if match:
        return match.group(1), match.group(2)
    return None


def main() -> None:
    print("Starting automatic migration fixer...\n")
    while True:
        code, out = run_manage("migrate")
        if code == 0:
            print("✅  All migrations applied successfully!")
            break

        if not has_duplicate_error(out):
            # Unexpected error, print and exit.
            print("❌  Migration failed with an unexpected error:\n")
            print(out)
            sys.exit(code or 1)

        offending = extract_offending_migration(out)
        if not offending:
            print("❌  Could not detect offending migration. Output:\n")
            print(out)
            sys.exit(1)

        app, migration = offending
        print(
            f"⚠️  Duplicate error detected while applying {app}.{migration}. "
            "Marking it as fake and retrying..."
        )
        fake_code, fake_out = run_manage("migrate", app, migration, "--fake")
        if fake_code != 0:
            print("❌  Failed to fake migration. Output:\n")
            print(fake_out)
            sys.exit(fake_code)
        else:
            print(f"👉  Successfully faked {app}.{migration}. Continuing...\n")


if __name__ == "__main__":
    main() 
