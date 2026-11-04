# Installation Guide

This guide installs the official Android Emulator on macOS without Android Studio.

## 1. Check your Mac

```bash
uname -m
sw_vers
df -h /
python3 --version
```

- `arm64`: Apple Silicon.
- `x86_64`: Intel.

The CLI selects `arm64-v8a` on Apple Silicon and `x86_64` on Intel.

## 2. Install Java

JDK 17 is recommended:

```bash
brew install --cask temurin@17
java -version
```

If Java is still not found, open a new Terminal session and inspect:

```bash
/usr/libexec/java_home -V
```

## 3. Clone the project

```bash
git clone https://github.com/itrunks/android-emulator-cli.git
cd android-emulator-cli
```

## 4. Run diagnostics and setup

```bash
python3 android_emulator.py doctor
python3 android_emulator.py setup
```

Setup checks macOS, Java and disk space; downloads Google's current macOS command-line tools; installs SDK Platform Tools, Emulator, API 35 platform/build tools and a Google APIs system image; configures `~/.zshrc`; and creates `Pixel_API_35`.

## 5. Reload shell and launch

Open a new Terminal window or run `source ~/.zshrc`, then:

```bash
echo "$ANDROID_HOME"
command -v adb
command -v emulator
python3 android_emulator.py start
```

In another Terminal:

```bash
android-emulator devices
```

## 6. Install an APK

```bash
android-emulator install-apk /absolute/path/to/app-debug.apk
```

## SDK directory

`~/Library/Android/sdk/` contains `cmdline-tools/latest`, `emulator`, `platform-tools`, `platforms`, `build-tools` and `system-images`.

## Uninstall

Stop emulators first. Review and back up any AVD data you need. Remove the SDK directory and the Android environment block from `~/.zshrc` manually. There is no automated uninstall command.
