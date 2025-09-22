[app]

# (str) Title of your application
title = Food Allergy Database

# (str) Package name
package.name = allergydatabase

# (str) Package domain (needed for android/ios packaging)
package.domain = com.wncc.allergydatabase

# (str) Source code where the main.py lives
source.dir = .

# (str) Main module to start from
source.main = allergy_database.py

# (list) Patterns to match files or directories to include
source.include_exts = py,png,jpg,kv,atlas,txt,db,csv

# (str) Application versioning
version = 1.0
# Android version code (increment for each Play Store release)
android.version_code = 1
# Version name used for release tagging
package.version = 1.0.0

# (list) Application requirements
## Pin a compatible Python version and Kivy. sqlite3 is included in Python's stdlib
requirements = python3==3.11,kivy==2.3.1

# (str) Android app theme
android.theme = "@android:style/Theme.NoTitleBar"

# (int) Android API to use
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 33

# (str) Android build tools version to use
android.build_tools = 34.0.0

# (bool) Enable AndroidX support
android.enable_androidx = True

# (bool) Automatically accept SDK licenses
android.accept_sdk_license = True

# (list) Permissions
## Updated permissions for modern Android versions
android.permissions = INTERNET

# (str) Icon for the application
icon.filename = icon.png

# (str) Presplash image (shown while loading)
presplash.filename = presplash.png

# Signing configuration for release builds. For CI, set the keystore as a
# base64-encoded GitHub secret and decode it during the workflow.
# Uncomment and fill these to use local signing instead of CI secrets.
# android.release_keystore = myrelease.keystore
# android.release_keyalias = mykeyalias
# android.release_keystore_pass = changeme
# android.release_keypass = changeme

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (str) Path to build directory (optional, defaults to ./bin)
# bin_dir = ./bin

# (str) Path to buildozer temporary directory (optional, defaults to ./.buildozer)
# cache_dir = ./.buildozer

# (bool) Automatically accept all Android SDK licenses
android.accept_all_sdk_licenses = True

# (str) Override the default android directory (optional)
# android.p4a_dir = ~/my-p4a-clone
