# Configuration

Current defaults are constants near the top of `android_emulator.py`:

| Constant | Default | Purpose |
|---|---|---|
| `SDK` | `~/Library/Android/sdk` | SDK root |
| `API` | `35` | Android API level |
| `AVD_NAME` | `Pixel_API_35` | Virtual device name |
| `MIN_FREE_GB` | `10` | Low-space warning threshold |

Change these constants before setup to customize the SDK location, API level, AVD name or disk threshold. Ensure the shell environment matches a custom SDK path.

The setup adds these exports to `~/.zshrc`:

```bash
export ANDROID_HOME="$HOME/Library/Android/sdk"
export PATH="$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_HOME/cmdline-tools/latest/bin"
```

Open a new Terminal session or run `source ~/.zshrc` after setup.
