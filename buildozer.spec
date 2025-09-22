[app]

# (str) Title of your application
title = Food Allergy Database

# (str) Package name
package.name = allergydatabase

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py lives
source.dir = .

# (str) Main module to start from
source.main = allergy_database.py

# (list) Patterns to match files or directories to include
source.include_exts = py,png,jpg,kv,atlas,txt,db

# (str) Application versioning
version = 1.0
# Android version code (increment for each Play Store release)
android.version_code = 1
# Version name used for release tagging
package.version = 1.0.0

# (list) Application requirements
## Pin a Kivy version compatible with your runtime. python-for-android will
## install the matching dependencies. sqlite3 is included in Python's stdlib
## so it does not need a separate recipe.
requirements = python3,kivy==2.3.1

# (str) Android app theme
android.theme = "@android:style/Theme.NoTitleBar"

# (int) Android API to use
android.api = 31

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Enable AndroidX support
android.enable_androidx = True

# (list) Permissions
## Common runtime permissions; add more if your app needs them.
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# (str) Icon for the application
icon.filename = icon.png

# (str) Presplash image (shown while loading)
presplash.filename = presplash.png

# (str) Presplash of the application
#presplash.filename = presplash.png

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
