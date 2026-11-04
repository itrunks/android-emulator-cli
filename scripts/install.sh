#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
command -v python3 >/dev/null 2>&1 || {
  echo "Python 3 is required"
  exit 1
}

BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

cat > "$BIN_DIR/android-emulator" <<EOF
#!/usr/bin/env bash
exec python3 "$ROOT/android_emulator.py" "\$@"
EOF
chmod +x "$BIN_DIR/android-emulator"

ZSHRC="$HOME/.zshrc"
if ! grep -q 'added by android_emulator_cli' "$ZSHRC" 2>/dev/null; then
  {
    echo
    echo "# Android Emulator CLI (added by android_emulator_cli)"
    echo 'export PATH="$HOME/.local/bin:$PATH"'
  } >> "$ZSHRC"
fi

echo "Installed command: $BIN_DIR/android-emulator"
echo "Reload your shell with: source ~/.zshrc"
echo "Then launch Pixel with: android-emulator launch pixel"

cd "$ROOT"
python3 android_emulator.py doctor
echo
echo "Starting Android SDK setup..."
python3 android_emulator.py setup
