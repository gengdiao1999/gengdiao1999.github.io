"""Batch generate figures for the book.

Walks through every chapter under book/ and runs Python scripts in
assets/code/ that match the naming convention <chapter>-example-*.py.

Usage:
    python3 tools/generate_figures.py
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
BOOK_DIR = REPO_ROOT / "book"


def main():
    scripts = sorted(BOOK_DIR.rglob("assets/code/*-example-*.py"))
    if not scripts:
        print("No figure generation scripts found.")
        return 0

    failures = []
    for script in scripts:
        print(f"Running {script.relative_to(REPO_ROOT)} ...")
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=script.parent,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            failures.append(script)
        else:
            print("OK")

    if failures:
        print("\nFailures:")
        for f in failures:
            print(f"  {f.relative_to(REPO_ROOT)}")
        return 1

    print(f"\nGenerated figures from {len(scripts)} script(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
