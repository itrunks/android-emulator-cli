#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
command -v python3 >/dev/null 2>&1 || {
  echo "Python 3 is required"
  exit 1
}

cd "$ROOT"
python3 android_emulator.py doctor
python3 android_emulator.py setup
