CI release workflow and required secrets

Required repository secrets (set these in your GitHub repo Settings > Secrets):

- ANDROID_KEYSTORE_BASE64: Base64-encoded keystore file contents (use `base64 release.keystore` to produce this value).
- KEYSTORE_PASSWORD: Password for the keystore (android.release_keystore_pass).
- KEY_ALIAS: Key alias used inside the keystore (android.release_keyalias).
- KEY_PASSWORD: Password for the key (android.release_keypass).

How the workflow works
- The workflow triggers on push tags matching `v*` (e.g., `v1.0.0`).
- It decodes the `ANDROID_KEYSTORE_BASE64` secret into `release.keystore` and runs `buildozer android release`.
- The signed AAB/APK artifact is uploaded as an artifact named `release-aab`.

Notes
- Ensure your `buildozer.spec` has the correct package.name and package.domain; you'll also want to bump `android.version_code` for each release.
- For debugging, you can run the same build steps locally in WSL or a Linux VM.
