#!/usr/bin/env python3
"""
Android Emulator CLI for macOS.

Bootstraps Google's Android command-line tools, installs SDK packages,
creates an AVD, and provides common emulator/ADB operations.
"""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

SDK = Path.home() / "Library" / "Android" / "sdk"
API = "35"
AVD_NAME = "Pixel_API_35"
REPO_XML = "https://dl.google.com/android/repository/repository2-3.xml"
MIN_FREE_GB = 10


def run(command: list[str], *, check: bool = True, input_text: str | None = None):
    """Run a command and print it for transparency."""
    print("\n$ " + " ".join(str(item) for item in command))
    return subprocess.run(
        [str(item) for item in command],
        check=check,
        text=True,
        input=input_text,
    )


def require_macos():
    if sys.platform != "darwin":
        raise SystemExit("This setup tool currently supports macOS only.")


def host_arch() -> str:
    """Return the Android ABI matching the current Mac architecture."""
    machine = platform.machine().lower()
    if machine in ("arm64", "aarch64"):
        return "arm64-v8a"
    if machine in ("x86_64", "amd64"):
        return "x86_64"
    raise SystemExit(f"Unsupported Mac architecture: {machine}")


def sdk_host_arch() -> str:
    """Return the Android repository host-arch label for this Mac."""
    machine = platform.machine().lower()
    if machine in ("arm64", "aarch64"):
        return "aarch64"
    if machine in ("x86_64", "amd64"):
        return "x64"
    raise SystemExit(f"Unsupported Mac architecture: {machine}")


def sdk_bin(name: str) -> Path:
    return SDK / "cmdline-tools" / "latest" / "bin" / name


def ensure_java():
    java = shutil.which("java")
    if not java:
        raise SystemExit(
            "Java was not found. Install JDK 17 first, for example with:\n"
            "  brew install --cask temurin@17\n"
            "Then open a new Terminal and run this tool again."
        )
    result = subprocess.run(["java", "-version"], text=True, capture_output=True)
    version_text = result.stderr + result.stdout
    print("Java detected:")
    print(version_text.strip().splitlines()[0] if version_text.strip() else java)


def download_cmdline_tools():
    """Download the official macOS command-line tools for this CPU architecture."""
    print("Fetching official Android SDK repository metadata...")
    request = urllib.request.Request(
        REPO_XML, headers={"User-Agent": "AndroidEmulatorCLI/1.0"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    preferred_url = None
    fallback_url = None
    target_arch = sdk_host_arch()

    for package in root.findall(".//remotePackage"):
        if package.attrib.get("path") != "cmdline-tools;latest":
            continue
        for archive in package.findall(".//archive"):
            host = archive.find("host-os")
            if host is None or (host.text or "").strip() != "macosx":
                continue

            complete = archive.find("complete")
            url_node = complete.find("url") if complete is not None else None
            if url_node is None or not url_node.text:
                continue

            candidate_url = urllib.parse.urljoin(
                "https://dl.google.com/android/repository/",
                url_node.text.strip(),
            )
            archive_arch = archive.find("host-arch")
            if archive_arch is None:
                fallback_url = fallback_url or candidate_url
            elif (archive_arch.text or "").strip() == target_arch:
                preferred_url = candidate_url
                break

        break

    archive_url = preferred_url or fallback_url
    if not archive_url:
        raise SystemExit(
            f"Could not locate Google's macOS command-line-tools archive for {target_arch}. "
            "Download it manually from "
            "https://developer.android.com/studio#command-line-tools-only"
        )

    SDK.mkdir(parents=True, exist_ok=True)
    tools_parent = SDK / "cmdline-tools"
    tools_parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="android-cli-") as temp_dir:
        temp_path = Path(temp_dir)
        archive_path = temp_path / "cmdline-tools.zip"
        print(f"Downloading: {archive_url}")
        urllib.request.urlretrieve(archive_url, archive_path)

        extract_dir = temp_path / "extracted"
        extract_dir.mkdir()
        with zipfile.ZipFile(archive_path) as archive:
            # Validate archive paths before extracting.
            for member in archive.infolist():
                target = (extract_dir / member.filename).resolve()
                if not target.is_relative_to(extract_dir.resolve()):
                    raise SystemExit("Unsafe path found in downloaded tools archive.")
            archive.extractall(extract_dir)

        source = extract_dir / "cmdline-tools"
        if not (source / "bin" / "sdkmanager").exists():
            candidates = list(extract_dir.rglob("sdkmanager"))
            if not candidates:
                raise SystemExit("Downloaded archive did not contain sdkmanager.")
            source = candidates[0].parent.parent

        destination = tools_parent / "latest"
        if destination.exists():
            print(f"Replacing existing command-line tools directory: {destination}")
            shutil.rmtree(destination)
        shutil.move(str(source), str(destination))

    print(f"Command-line tools installed at: {tools_parent / 'latest'}")


def configure_environment():
    zshrc = Path.home() / ".zshrc"
    block = (
        "\n# Android SDK (added by android_emulator_cli)\n"
        f'export ANDROID_HOME="{SDK}"\n'
        'export PATH="$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:'
        '$ANDROID_HOME/cmdline-tools/latest/bin"\n'
    )
    existing = zshrc.read_text() if zshrc.exists() else ""
    if "added by android_emulator_cli" not in existing:
        with zshrc.open("a") as file:
            file.write(block)
        print(f"Added Android SDK environment variables to {zshrc}")
    else:
        print("Android SDK environment variables are already in ~/.zshrc")


def check_disk():
    SDK.parent.mkdir(parents=True, exist_ok=True)
    free_gb = shutil.disk_usage(Path.home()).free / (1024 ** 3)
    print(f"Available disk space: {free_gb:.1f} GB")
    if free_gb < MIN_FREE_GB:
        answer = input(
            f"Warning: less than {MIN_FREE_GB} GB is available. Continue anyway? [y/N] "
        ).strip().lower()
        if answer != "y":
            raise SystemExit("Stopped before downloading or installing anything.")


def sdkmanager() -> Path:
    path = sdk_bin("sdkmanager")
    if not path.exists():
        download_cmdline_tools()
    if not path.exists():
        raise SystemExit(f"sdkmanager was not found at expected path: {path}")
    return path


def install_sdk():
    require_macos()
    ensure_java()
    check_disk()

    manager = sdkmanager()
    arch = host_arch()
    image = f"system-images;android-{API};google_apis;{arch}"
    packages = [
        "platform-tools",
        "emulator",
        f"platforms;android-{API}",
        f"build-tools;{API}.0.0",
        image,
    ]

    print(f"\nMac architecture: {platform.machine()} ({arch})")
    print(f"SDK location: {SDK}")
    print("\nReview and accept the Android SDK licence terms when prompted:")
    run([manager, f"--sdk_root={SDK}", "--licenses"])

    print(f"\nInstalling Android API {API} packages...")
    run([manager, f"--sdk_root={SDK}", *packages])

    configure_environment()
    create_avd(image)
    print("\nSetup completed.")
    print("Open a new Terminal, then run:")
    print("  python3 android_emulator.py start")
    print(f"SDK path: {SDK}")


def create_avd(image: str | None = None):
    require_macos()
    avdmanager = sdk_bin("avdmanager")
    if not avdmanager.exists():
        raise SystemExit("avdmanager is missing. Run: python3 android_emulator.py setup")

    image = image or f"system-images;android-{API};google_apis;{host_arch()}"
    listing = subprocess.run(
        [str(avdmanager), "list", "avd"], text=True, capture_output=True
    )
    if AVD_NAME in listing.stdout:
        print(f"AVD already exists: {AVD_NAME}")
        return

    run(
        [
            avdmanager,
            "--verbose",
            "create",
            "avd",
            "-n",
            AVD_NAME,
            "-k",
            image,
            "-f",
        ],
        input_text="no\n",
    )
    print(f"Created AVD: {AVD_NAME}")


def emulator_path() -> Path:
    path = SDK / "emulator" / "emulator"
    if not path.exists():
        raise SystemExit("Emulator is not installed. Run: python3 android_emulator.py setup")
    return path


def start_emulator():
    require_macos()
    run([emulator_path(), "-avd", AVD_NAME])


def stop_emulator():
    adb = SDK / "platform-tools" / "adb"
    if not adb.exists():
        raise SystemExit("ADB is not installed. Run setup first.")
    run([adb, "emu", "kill"], check=False)


def list_devices():
    adb = SDK / "platform-tools" / "adb"
    if not adb.exists():
        raise SystemExit("ADB is not installed. Run setup first.")
    run([adb, "devices", "-l"])


def install_apk(apk: Path):
    adb = SDK / "platform-tools" / "adb"
    if not adb.exists():
        raise SystemExit("ADB is not installed. Run setup first.")
    if not apk.is_file() or apk.suffix.lower() != ".apk":
        raise SystemExit(f"APK file not found or not an .apk file: {apk}")
    run([adb, "install", "-r", apk])


def doctor():
    require_macos()
    print(f"Mac: {platform.machine()}")
    print(f"SDK: {SDK}")
    print(f"SDK directory exists: {SDK.exists()}")
    print(f"Command-line tools: {sdk_bin('sdkmanager').exists()}")
    print(f"Emulator: {(SDK / 'emulator' / 'emulator').exists()}")
    print(f"ADB: {(SDK / 'platform-tools' / 'adb').exists()}")
    print(f"Free disk: {shutil.disk_usage(Path.home()).free / (1024 ** 3):.1f} GB")
    java = shutil.which("java")
    print(f"Java: {java or 'not found'}")
    if java:
        subprocess.run([java, "-version"], check=False)


def main():
    parser = argparse.ArgumentParser(
        description="Install and manage an Android Emulator on macOS."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("setup", help="Install SDK tools, Android API image and create Pixel AVD")
    sub.add_parser("start", help="Start the Pixel emulator")
    sub.add_parser("stop", help="Stop the running emulator")
    sub.add_parser("devices", help="List connected Android devices")
    sub.add_parser("doctor", help="Check the local setup")
    apk_parser = sub.add_parser("install-apk", help="Install an APK on the running emulator")
    apk_parser.add_argument("apk", type=Path)

    args = parser.parse_args()
    if args.command == "setup":
        install_sdk()
    elif args.command == "start":
        start_emulator()
    elif args.command == "stop":
        stop_emulator()
    elif args.command == "devices":
        list_devices()
    elif args.command == "doctor":
        doctor()
    elif args.command == "install-apk":
        install_apk(args.apk.expanduser().resolve())


if __name__ == "__main__":
    main()
