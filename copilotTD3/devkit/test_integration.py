#!/usr/bin/env python
"""Integration test script for devkit."""

import subprocess
import sys


def run_command(cmd: str) -> int:
    """Run command and return exit code."""
    print(f"\n{'='*60}")
    print(f"$ {cmd}")
    print(f"{'='*60}")
    return subprocess.call(cmd, shell=True)


def main() -> int:
    """Run integration tests."""
    tests = [
        # Basic CLI tests
        ("devkit --version", "Show version"),
        ("devkit --help", "Show main help"),
        ("devkit gh --help", "Show GitHub commands help"),
        ("devkit ai --help", "Show AI commands help"),
        ("devkit workflow --help", "Show workflow commands help"),
        # Individual command help
        ("devkit gh issues --help", "Show issues command help"),
        ("devkit ai explain --help", "Show explain command help"),
        ("devkit workflow feature-start --help", "Show feature-start command help"),
    ]

    print("\n" + "="*60)
    print("DEVKIT INTEGRATION TESTS")
    print("="*60)

    failed = 0
    for cmd, desc in tests:
        print(f"\n[TEST] {desc}")
        if run_command(cmd) != 0:
            print(f"✗ FAILED: {desc}")
            failed += 1
        else:
            print(f"✓ PASSED: {desc}")

    print("\n" + "="*60)
    print(f"Results: {len(tests) - failed}/{len(tests)} passed")
    print("="*60 + "\n")

    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
