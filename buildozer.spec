[app]

# (str) Title of your application
title = Food Allergy Shield

# (str) Package name
package.name = foodallergyshield

# (str) Package domain (needed for android/ios packaging)
package.domain = com.billthecomputerguy.foodallergyshield

# (str) Source code where the main.py lives
source.dir = .

# (str) Main module to start from
source.main = food_allergy_shield.py

# (list) Patterns to match files or directories to include
source.include_exts = py,png,jpg,kv,atlas,txt,db,csv

# (str) Application versioning
version = 0.1
# Android version code (increment for each Play Store release)
android.version_code = 1
# Version name used for release tagging
package.version = 0.1.0

# (list) Application requirements
## Pin a compatible Python version and Kivy. sqlite3 is included in Python's stdlib
requirements = python3,kivy

# (str) Bootstrap to use for android builds
android.bootstrap = sdl2

# (str) Android app theme
android.theme = "@android:style/Theme.NoTitleBar"

# (int) Android API to use
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b
# Alternative: use latest available NDK
# android.ndk = 27c

# (str) Android build tools version to use
android.build_tools = 33.0.2

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

# (str) python-for-android fork to use (optional)
p4a.fork = kivy

# (str) python-for-android branch to use (optional)
p4a.branch = develop

# (str) python-for-android git url (if not fork)
# p4a.url = https://github.com/kivy/python-for-android.git

# (bool) Whether to use --private data storage
# android.private_storage = True

# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a
