[app]
# (str) Title of your application
title = Food Allergy Database

# (str) Package name
package.name = allergydatabase

# (str) Package domain (needed for Android/iOS)
# IMPORTANT: Change this to a domain you control, e.g., com.mycompany
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let buildozer find them)
# source.include_exts = py,png,jpg,kv,atlas
# We need to include .py, .kv, and image files.
# The app also uses a database file, but it's created at runtime.
source.include_exts = py,kv,png,jpg,gif,atlas

# (list) List of modules to exclude from the package
# source.exclude_dirs = tests, bin, venv, .github, tools

# (str) Application versioning
version = 0.1

# (list) Kivy requirements
# Pinning versions is a good practice for reproducible builds.
# Your README mentions Kivy 2.3.1.
requirements = python3,kivy==2.3.1

# (str) Custom application icon (path to an image)
icon.filename = %(source.dir)s/icon.png

# (str) Custom application presplash image (path to an image)
presplash.filename = %(source.dir)s/presplash.png

# (str) Presplash background color (for areas not covered by the image)
# presplash.color = #FFFFFF

# (str) Application orientation
# 'portrait', 'landscape', 'all'
orientation = portrait

# (list) Permissions
# Your app only deals with local files, so no special permissions are needed.
# android.permissions =

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0


[buildozer]
# (int) Log level (0 = error, 1 = info, 2 = debug (very verbose))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1


#-----------------------------------------------------------------------------
# Android specific settings
#
[android]

# (int) Android API to use.
# Google Play requires API 33+ for new apps/updates as of late 2023.
android.api = 33

# (int) Minimum API required
# API 21 is a good baseline, covering ~99% of devices.
android.minapi = 21

# (str) Android NDK version to use
# Leaving this commented out lets buildozer use a default, stable version.
# android.ndk = 25b

# (list) Android architectures to build for.
# arm64-v8a is required for Google Play.
android.archs = arm64-v8a, armeabi-v7a

# (str) The Android SDK version to use
# android.sdk = 24

# (str) The Android build tools version to use
# android.build_tools = 33.0.1

# (str) python-for-android branch to use
p4a.branch = master

# (str) Path to a custom keystore for release signing
# These are best set by environment variables in CI, as you are already doing.
# android.release_keystore =
# android.release_key_alias =
# android.keystore_pass =
# android.key_alias_pass =

# (bool) Copy library files to build-dir/libs
# Set to True if you have problems with shared libraries not being found.
# android.copy_libs = 1

# (list) The Android services to declare.
# services =