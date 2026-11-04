# Contributing

Thanks for considering a contribution.

1. Open an issue describing the bug or enhancement.
2. Keep pull requests focused and update documentation and `CHANGELOG.md`.
3. Test on the macOS architecture available to you.

## Local checks

```bash
python3 -m py_compile android_emulator.py
python3 android_emulator.py --help
python3 android_emulator.py doctor
```

Do not run the full setup workflow in CI unless the runner has sufficient disk space and the required macOS environment.

Include the change rationale, macOS version/architecture, commands run and relevant redacted output in pull requests.
