# Command Reference

After running `./scripts/install.sh`, use the globally installed command:

```bash
android-emulator <command>
```

## Launch Pixel

The shortest everyday command is:

```bash
android-emulator launch pixel
```

## Other commands

| Command | Description |
|---|---|
| `android-emulator doctor` | Inspect macOS, architecture, SDK paths, emulator, ADB, disk and Java |
| `android-emulator setup` | Install command-line tools and SDK packages, then create the default AVD |
| `android-emulator launch pixel` | Launch the Pixel API 35 virtual device |
| `android-emulator stop` | Stop the running emulator |
| `android-emulator devices` | List physical and virtual devices |
| `android-emulator install-apk <path>` | Install or replace an APK on a connected device |

The original Python entry point remains available for development:

```bash
python3 android_emulator.py launch pixel
python3 android_emulator.py doctor
```
