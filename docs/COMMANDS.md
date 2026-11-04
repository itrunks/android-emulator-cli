# Command Reference

Run from the repository directory using `python3 android_emulator.py <command>`.

| Command | Description |
|---|---|
| `doctor` | Inspect macOS, architecture, SDK paths, emulator, ADB, disk and Java |
| `setup` | Install command-line tools and SDK packages, then create the default AVD |
| `start` | Launch `Pixel_API_35` |
| `stop` | Stop the emulator through ADB |
| `devices` | List physical and virtual devices |
| `install-apk <path>` | Install or replace an APK on a connected device |

Examples:

```bash
python3 android_emulator.py doctor
python3 android_emulator.py setup
python3 android_emulator.py start
python3 android_emulator.py devices
python3 android_emulator.py install-apk ~/Downloads/app-debug.apk
python3 android_emulator.py stop
```

The emulator must be running and visible to ADB before installing an APK.
