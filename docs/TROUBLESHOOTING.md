# Troubleshooting

## Java not found

```bash
brew install --cask temurin@17
java -version
/usr/libexec/java_home -V
```

Open a new Terminal after installing Java.

## sdkmanager / avdmanager missing

```bash
ls -la ~/Library/Android/sdk/cmdline-tools/latest/bin
```

The `latest` folder should contain `bin`, `lib` and metadata files. The extracted command-line tools contents belong inside `cmdline-tools/latest`.

## adb not found

```bash
source ~/.zshrc
command -v adb
~/Library/Android/sdk/platform-tools/adb devices
```

## Emulator fails to start

Run `python3 android_emulator.py doctor`; verify the AVD with `avdmanager list avd`, confirm the emulator binary exists, check disk space and restart the AVD.

## ADB device is offline

```bash
adb kill-server
adb start-server
adb devices -l
```

Wait for Android to finish booting.

## APK installation fails

```bash
file ~/Downloads/app-debug.apk
adb devices
adb install -r ~/Downloads/app-debug.apk
```

Check APK ABI and minimum Android API compatibility.

## Low disk space

```bash
df -h /
du -sh ~/Library/Android/sdk 2>/dev/null
```

Do not delete Xcode DerivedData or SDK directories blindly. Review exact contents first.

## Still failing

Open a GitHub issue with macOS version, CPU architecture, Python/Java versions, `doctor` output and full error text. Redact sensitive paths or data.
