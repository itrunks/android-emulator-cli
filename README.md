# Android Emulator CLI

A lightweight Python command-line tool to install, configure, launch, and manage the official Android Emulator on macOS — without installing Android Studio.

> **Release:** v1.0.0  
> **Platforms:** macOS Apple Silicon (ARM64) and Intel (x86_64)  
> **License:** MIT

## Features

- Detects Apple Silicon vs Intel architecture.
- Downloads Google's official Android SDK Command-line Tools.
- Installs Android SDK Platform Tools, Emulator, Platform, Build Tools, and a Google APIs system image.
- Creates a configurable Pixel virtual device.
- Starts and stops the emulator from the terminal.
- Lists connected devices through ADB.
- Installs APK files on the running emulator.
- Provides a diagnostic command for common setup checks.
- Does not require Android Studio.

## Requirements

- macOS 13 or later recommended.
- Python 3.10 or later.
- JDK 17 or later available as `java`.
- Internet access.
- At least 10 GB of free disk space recommended.

## Quick start

1. Install JDK 17 if needed:

   ```bash
   brew install --cask temurin@17
   ```

2. Clone this repository:

   ```bash
   git clone https://github.com/itrunks/android-emulator-cli.git
   cd android-emulator-cli
   ```

3. Run diagnostics:

   ```bash
   python3 android_emulator.py doctor
   ```

4. Install the Android SDK components and create the default virtual device:

   ```bash
   python3 android_emulator.py setup
   ```

5. Open a new Terminal window, then start the emulator:

   ```bash
   android-emulator launch pixel
   ```

## Commands

| Command | Description |
|---|---|
| `setup` | Install SDK packages and create the default AVD |
| `doctor` | Inspect Java, SDK paths, installed tools, and free disk space |
| `launch pixel` | Launch the Pixel virtual device with one command |
| `start` | Legacy alias for launching the default Pixel device |
| `stop` | Stop the running emulator |
| `devices` | List connected devices with ADB |
| `install-apk <path>` | Install or replace an APK on the connected emulator |

After running `scripts/install.sh`, the `android-emulator` command is installed in `~/.local/bin`. Ensure that directory is on your shell `PATH` (the installer adds it to `~/.zshrc`).

## Default configuration

| Setting | Default |
|---|---|
| Android SDK directory | `~/Library/Android/sdk` |
| Android API level | 35 |
| AVD name | `Pixel_API_35` |
| System image | `google_apis` |
| Apple Silicon ABI | `arm64-v8a` |
| Intel ABI | `x86_64` |

Edit the constants near the top of `android_emulator.py` to customize the API level, AVD name, or SDK location.

## Documentation

- [Installation guide](docs/INSTALLATION.md)
- [Command reference](docs/COMMANDS.md)
- [Configuration](docs/CONFIGURATION.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Changelog](CHANGELOG.md)
- [Release notes](RELEASE_NOTES.md)
- [Contributing](CONTRIBUTING.md)

## Safety and behaviour

- The tool does not use `sudo`.
- It does not delete an existing Android SDK directory.
- If `cmdline-tools/latest` already exists, setup replaces that specific directory while installing the current command-line tools.
- Review the SDK directory before running setup if it contains a manually customized command-line tools installation.
- Android SDK licences are presented for acceptance; accept them only if you agree to Google's terms.
- Downloads come from Google's official Android SDK repository.

## Limitations

- macOS only; Windows and Linux are not currently supported.
- One default AVD is created by the setup workflow.
- API 35 is the initial default.
- This is a command-line setup and management utility, not an AI agent or Android app test runner.

## License

Distributed under the MIT License. See [LICENSE](LICENSE).
