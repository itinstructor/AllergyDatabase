Android build instructions for Food Allergy Database

Prereqs (recommended environment)
- Ubuntu 20.04+ or WSL2 with Ubuntu installed (buildozer and python-for-android work best on Linux).
- Python 3.11+ installed on the host (inside WSL/Ubuntu). Use a virtualenv.
- Java JDK 11 (OpenJDK 11) installed in the build environment.
- Android SDK & NDK will be installed automatically by buildozer (or preinstall them for faster builds).

Quick steps (WSL/Linux)

1. Install system deps (Ubuntu example):

   sudo apt update; sudo apt install -y python3-venv python3-pip git zip unzip openjdk-11-jdk

2. Create and activate a virtualenv:

   python3 -m venv venv; . venv/bin/activate

3. Install buildozer and dependencies:

   pip install --upgrade pip
   pip install buildozer

4. From the project root (where `buildozer.spec` lives), run:

   buildozer android debug

   The first build will download the Android SDK/NDK and take a while. Subsequent
   builds are much faster.

Notes for Windows users
- Buildozer isn't supported natively on Windows. Use WSL2 (recommended) or a Linux VM.
- If you must use Windows, consider using a remote Linux builder or GitHub Actions CI that runs the build in Linux.

Common issues
- If buildozer cannot find `python3` or pip in the path, ensure your virtualenv is activated.
- If builds fail with NDK errors, try using a stable `android.ndk` value in `buildozer.spec` (e.g., `21d`), or install the matching NDK manually.

If you want, I can:
- Add a simple GitHub Actions workflow to build an APK automatically on push.
- Prepare an icon and presplash images and wire them into `buildozer.spec`.
