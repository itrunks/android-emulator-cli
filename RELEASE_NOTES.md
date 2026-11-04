# Android Emulator CLI v1.0.0

**Release date:** 2026-11-04  
**Release type:** Initial public release

## Highlights

Install and manage the official Android Emulator on macOS from the terminal without installing Android Studio.

## Included
- One-command Pixel launch: `android-emulator launch pixel` after running `./scripts/install.sh`.
- Global `android-emulator` launcher installed in `~/.local/bin`.

- macOS architecture detection (Apple Silicon / Intel)
- Java and disk-space preflight checks
- Google SDK command-line tools bootstrap
- Platform Tools, Emulator, API 35 platform/build tools and Google APIs system image
- Default Pixel API 35 AVD creation
- Emulator start/stop, ADB devices, APK installation and diagnostics
- Installation and troubleshooting documentation

## Requirements

macOS, Python 3, JDK 17 or later, internet access and 10 GB free disk space recommended.

## Known limitations

- macOS only.
- One default AVD is created by the setup workflow.
- API 35 is the initial default.
- This is a setup and lifecycle utility, not a full Android application test runner.
