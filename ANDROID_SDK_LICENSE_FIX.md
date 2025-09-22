# Android SDK License Resolution Guide

This guide provides solutions for Android SDK Build Tools licensing issues when building with buildozer.

## Problem
The error occurs when buildozer cannot install Android SDK Build Tools due to unaccepted licenses:
```
Accept? (y/N): Skipping following packages as the license is not accepted:
Android SDK Build-Tools 36.1
```

## Solutions Applied to buildozer.spec

### 1. Explicit Build Tools Version
Changed from the problematic version 36.1.0 to a stable version:
```ini
android.build_tools = 34.0.0
```

### 2. Automatic License Acceptance
Added configurations to automatically accept SDK licenses:
```ini
android.accept_sdk_license = True
android.accept_all_sdk_licenses = True
```

### 3. SDK Version Specification
Explicitly set the Android SDK version:
```ini
android.sdk = 31
```

## Manual Resolution Steps (if needed)

If the automatic license acceptance doesn't work, you can manually accept licenses:

### Option 1: Using buildozer commands
```bash
# Clean buildozer cache and rebuild
buildozer android clean

# Accept licenses during rebuild
buildozer android debug
```

### Option 2: Direct SDK Manager (if you have Android Studio)
```bash
# Navigate to Android SDK location
cd $ANDROID_HOME/tools/bin

# List and accept all licenses
./sdkmanager --licenses
```

### Option 3: Environment Variable (for CI/CD)
Set environment variable to automatically accept licenses:
```bash
export ANDROID_ACCEPT_SDK_LICENSE=y
```

## Recommended buildozer.spec Configuration

The following configuration should resolve most Android SDK licensing issues:

```ini
[app]
# ... your app configuration ...

# Android configuration
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31
android.build_tools = 34.0.0
android.accept_sdk_license = True
android.enable_androidx = True

[buildozer]
log_level = 2
android.accept_all_sdk_licenses = True
```

## Troubleshooting

1. **Clean build**: Always try `buildozer android clean` first
2. **Update buildozer**: Ensure you have the latest buildozer version
3. **Check permissions**: Ensure write permissions to the build directory
4. **Internet connection**: SDK downloads require stable internet

## Common Build Tools Versions
- **34.0.0** - Stable, recommended
- **33.0.0** - Alternative stable version
- **32.0.0** - Older but reliable
- **30.0.3** - Compatible with older projects

Avoid using very new versions (35.x, 36.x) as they may have compatibility issues with buildozer.