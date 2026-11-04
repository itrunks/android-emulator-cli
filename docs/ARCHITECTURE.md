# Architecture

The CLI is a Python standard-library wrapper around Google's Android SDK command-line utilities.

```text
User -> android_emulator.py
         |-- host checks: macOS / architecture / Java / disk
         |-- bootstrap: Google repository metadata / tools archive
         |-- sdkmanager: SDK packages and licences
         |-- avdmanager: virtual device creation
         |-- emulator: AVD lifecycle
         `-- adb: device listing, shutdown and APK installation
```

The host architecture selects `arm64-v8a` on Apple Silicon and `x86_64` on Intel. The default SDK root is the conventional per-user macOS SDK directory. No third-party Python packages or administrator privileges are required.

## Security

- Downloads come from Google's official SDK repository.
- Archive paths are validated before extraction.
- No credentials are requested or stored.
- The tool does not invoke `sudo`.
- Users should review SDK licences and organizational policies before installation.
