# FoodSafe (Kivy)

Benny the Bite 
A small cross-platform Kivy application to store food allergies in a local SQLite database, rate danger levels, and search ingredients.

Repository contents

- `allergy_database.py` — application logic and Kivy App
- `allergydatabase.kv` — KV layout (UI)
- `buildozer.spec` — Android packaging config
- `tools/generate_placeholders.py` — helper to create example `icon.png` and `presplash.png`
- `icon.png`, `presplash.png` — placeholder images (replace with production art before release)

Quick start — run on Windows

Requirements

- Python 3.10+ (3.13 used in development)
- Kivy 2.3.1

Install and run

```powershell
# Food Allergy Database (Kivy)

A small cross-platform Kivy application to store food allergies in a local SQLite database, rate danger levels, and search ingredients.

Repository contents

- `allergy_database.py` — application logic and Kivy App
- `allergydatabase.kv` — KV layout (UI)
- `buildozer.spec` — Android packaging config
- `tools/generate_placeholders.py` — helper to create example `icon.png` and `presplash.png`
- `icon.png`, `presplash.png` — placeholder images (replace with production art before release)

Quick start — run on Windows

Requirements

- Python 3.10+ (3.13 used in development)
- Kivy 2.3.1

Install and run

```powershell
python -m pip install kivy==2.3.1
python allergy_database.py
```

On first run the app creates `allergies.db` in the working directory.

App features

- Add allergy entries (name, danger level 1–4, symptoms, ingredients, notes)
- View a list of allergies (sorted by danger level)
- Search by allergen name or ingredients (case-insensitive)
- Delete entries with confirmation

Android build (local)

The project is prepared for Buildozer packaging. Build Android packages on Linux/WSL/macOS.

Basic local steps (WSL / Ubuntu example)

```bash
# install buildozer dependencies
sudo apt update && sudo apt install -y build-essential git python3-pip python3-virtualenv
pip install --user buildozer

# build (from repo root)
buildozer android debug
```

Notes

- `buildozer.spec` points at `icon.png` and `presplash.png` in the repository root. Update `icon.filename` / `presplash.filename` if you place assets elsewhere.
- For Play Store releases you must sign the build with a Java keystore. CI in this project can decode a base64 keystore secret; locally set `android.release_keystore`, `android.release_keyalias`, and key passwords in `buildozer.spec`.

Placeholder images

Generate example placeholders with:

```powershell
python tools/generate_placeholders.py
```

This writes `icon.png` (512×512) and `presplash.png` (2732×2732) to the repo root.

Troubleshooting

- If the app fails to start, verify Kivy is installed and check the console for tracebacks.
- If UI elements are duplicated, ensure `allergydatabase.kv` is present and the app is started from the repository root so Kivy can find and load the KV file.
- For Buildozer failures, run `buildozer -v android debug` and inspect the logs for missing recipes or toolchain errors.

Developer notes

- UI: KV-first approach — presentation in `allergydatabase.kv`, logic in `allergy_database.py`.
- Data: SQLite file `allergies.db` created in the working directory.
- Popup timeout: controlled by `UIConfig.success_popup_timeout` in `allergy_database.py`.

Want help next?

- I can add Play Store publishing automation to CI (requires Play service account keys).
- I can generate Android resource variants (mipmap) and update `buildozer.spec`.
- I can add unit tests for the `DatabaseManager`.

Generated on 2025-09-21

App features

- Add allergy entries (name, danger level 1–4, symptoms, ingredients, notes)
- View a list of allergies (sorted by danger level)
- Search by allergen name or ingredients (case-insensitive)
- Delete entries with confirmation

UI details

- The UI is defined in `allergydatabase.kv` to avoid duplication and keep layout portable between desktop and mobile
- `UIConfig` in `allergy_database.py` detects the platform and sets larger touch targets on mobile

Android build (local)

The project is prepared for Buildozer packaging. Build Android packages on Linux/WSL/macOS.

Basic local steps (WSL / Ubuntu example)

```bash
# install buildozer dependencies
sudo apt update && sudo apt install -y build-essential git python3-pip python3-virtualenv
pip install --user buildozer

# build (from repo root)
buildozer android debug
```

Notes

- `buildozer.spec` points at `icon.png` and `presplash.png` in the repository root. Update `icon.filename` / `presplash.filename` if you place assets elsewhere.
- For Play Store releases you must sign the build with a Java keystore. CI in this project uses a base64-encoded keystore secret; locally set `android.release_keystore`, `android.release_keyalias`, and key passwords in `buildozer.spec`.

Placeholder images

A small helper script generates the example images used in this repo:

```powershell
python tools/generate_placeholders.py
```

This writes `icon.png` (512×512) and `presplash.png` (2732×2732) to the repo root. Replace them with production artwork before release.

Troubleshooting

- If the app fails to start, verify Kivy is installed and check the console for tracebacks.
- If UI elements are duplicated, ensure `allergydatabase.kv` is present and the app is started from the repository root so Kivy can find and load the KV file.
- For Buildozer failures, run `buildozer -v android debug` and inspect the logs for missing recipes or toolchain errors.

Developer notes

- UI: KV-first approach — presentation in `allergydatabase.kv`, logic in `allergy_database.py`.
- Data: SQLite file `allergies.db` created in the working directory.
- Popup timeout: controlled by `UIConfig.success_popup_timeout` in `allergy_database.py`.

Want help next?

- I can add Play Store publishing automation to CI (requires Play service account keys).
- I can generate Android resource variants (mipmap) and update `buildozer.spec`.
- I can add unit tests for the `DatabaseManager`.

Generated on 2025-09-21


## 🎯 Project Overview

A cross-platform food allergy management application built with Kivy, featuring:

- SQLite database for persistent storage
- Responsive design for Windows and Android
- Search and filtering capabilities
- Danger level rating system (1-10 scale)
- Modern, user-friendly interface
- **Two Implementation Approaches**: Pure Python vs KV Language styling

## 📁 Project Structure

```text
AllergyDatabase/
├── allergy_database.py              # Original pure Python implementation
├── allergy_database_kv_fixed.py     # KV-styled implementation (RECOMMENDED)
├── allergydatabase_fixed.kv         # UI styling and layout definitions
├── sample_data.py                   # Database population script
├── buildozer.spec                   # Android build configuration
├── UI_APPROACHES_COMPARISON.md      # Detailed comparison guide
└── README.md                        # This summary
```

## 🚀 Quick Start

## How this app works (for beginners)

This short walkthrough explains the app architecture in plain terms:

- The app uses Kivy for the user interface and SQLite (a small file-based
   database) to store allergy records.
- The UI is split into separate screens (Main menu, Add, List, Search).
   We switch screens using a ScreenManager. Each Screen is defined by a
   Python class in `allergy_database.py` and its layout is described in the
   KV file `allergy_database.kv`.
- Widgets declared in the KV file get `id` names. From Python we can access
   those widgets with `self.ids.<id_name>` inside a Screen class.
- The `DatabaseManager` class opens `allergies.db`, creates the table on
   first run, and provides simple methods: `add_allergy`, `get_all_allergies`,
   `search_allergies`, and `delete_allergy`.
- Popups are used to show quick messages. The app auto-closes success
   popups after a short timeout so the user doesn't need to dismiss them.

Suggested quick experiment for learners:

1. Open `allergy_database.py` and find the `DatabaseManager.add_allergy` method. Add a print statement before the INSERT to see what data is being stored.
2. Run the app and add a sample allergy. Open `allergies.db` with the `sqlite3` command-line tool or a GUI SQLite browser to inspect the table.
3. Open `allergy_database.kv` and change the text on the main menu buttons. Save and re-run to see how KV changes the UI.


# Food Allergy Database (Kivy)

This repository contains a small cross-platform Kivy application that stores food allergies in a local SQLite database, lets you rate danger levels, and search ingredients.

Repository contents

- `allergy_database.py` — application logic and Kivy App
- `allergydatabase.kv` — KV layout (UI)
- `buildozer.spec` — Android packaging config
- `icon.png`, `presplash.png` — placeholder images (generated by `tools/generate_placeholders.py`)

Quick start — run on Windows

Requirements

- Python 3.10+ (3.13 used in development)
- Kivy 2.3.1

Install and run

```powershell
python -m pip install kivy==2.3.1
python allergy_database.py
```

On first run the app creates `allergies.db` in the working directory.

App features

- Add allergy entries (name, danger level 1–4, symptoms, ingredients, notes)
- View a list of allergies (sorted by danger level)
- Search by allergen name or ingredients (case-insensitive)
- Delete entries with confirmation

Android build (local)

The project is prepared for Buildozer packaging. Build Android packages on Linux/WSL/macOS.

Basic local steps (WSL / Ubuntu example)

```bash
# install buildozer dependencies
sudo apt update && sudo apt install -y build-essential git python3-pip python3-virtualenv
pip install --user buildozer

# build (from repo root)
buildozer android debug
```

Notes

- `buildozer.spec` points at `icon.png` and `presplash.png` in the repository root. Update `icon.filename` / `presplash.filename` if you place assets elsewhere.
- For Play Store releases you must sign the build with a Java keystore. CI in this project uses a base64-encoded keystore secret; locally set `android.release_keystore`, `android.release_keyalias`, and key passwords in `buildozer.spec`.

Placeholder images

Generate example placeholders with:

```powershell
python tools/generate_placeholders.py
```

This writes `icon.png` (512×512) and `presplash.png` (2732×2732) to the repo root. Replace them with production artwork before release.

Troubleshooting

- If the app fails to start, verify Kivy is installed and check the console for tracebacks.
- If UI elements are duplicated, ensure `allergydatabase.kv` is present and the app is started from the repository root so Kivy can find and load the KV file.
- For Buildozer failures, run `buildozer -v android debug` and inspect the logs for missing recipes or toolchain errors.

Developer notes

- UI: KV-first approach — presentation in `allergydatabase.kv`, logic in `allergy_database.py`.
- Data: SQLite file `allergies.db` created in the working directory.
- Popup timeout: controlled by `UIConfig.success_popup_timeout` in `allergy_database.py`.

Want help next?

- I can add Play Store publishing automation to CI (requires Play service account keys).
- I can generate Android resource variants (mipmap) and update `buildozer.spec`.
- I can add unit tests for the `DatabaseManager`.

Generated on 2025-09-21

  - **Low (1-4)** (Green): Minor reactions
- Add detailed descriptions of symptoms
- Automatically prevents duplicate entries

### **View All Allergies**

- Display all stored allergies with full details
- Color-coded danger level indicators
- Sort by allergen name or danger level
- Tap/click for detailed view
- Edit or delete individual entries

### **Search Ingredients**

- Real-time search as you type
- Case-insensitive matching
- Search through allergen names and descriptions
- Instant results filtering
- Clear search with single button press

## 🛠️ Installation & Setup

### **Prerequisites**

- Python 3.6+
- pip (Python package installer)

### **Quick Start**

1. Install dependencies:

   ```bash
   pip install kivy
   ```

2. Run the application:

   ```bash
   python allergy_database_kv_fixed.py
   ```

3. (Optional) Populate with sample data:

   ```bash
   python sample_data.py
   ```

### **Android Deployment**

1. Install Buildozer:

   ```bash
   pip install buildozer
   ```

2. Initialize and build APK:

   ```bash
   buildozer android debug
   ```

## 📊 Sample Data

The application includes 10 common food allergies:

- Peanuts (Danger: 9/10)
- Tree Nuts (Danger: 8/10)
- Shellfish (Danger: 8/10)
- Fish (Danger: 7/10)
- Milk (Danger: 6/10)
- Eggs (Danger: 6/10)
- Soy (Danger: 5/10)
- Wheat (Danger: 5/10)
- Sesame (Danger: 6/10)
- Sulfites (Danger: 4/10)

## 🎨 UI Design Highlights

### **Responsive Components:**

```kv
<CommonButton@Button>:
    font_size: sp(14)
    size_hint_y: None
    height: MOBILE_BUTTON_HEIGHT if app.ui_config.is_mobile else DESKTOP_BUTTON_HEIGHT
```

### **Platform Detection:**

```python
class UIConfig:
    def __init__(self):
        self.is_mobile = platform in ['android', 'ios']
        self.is_desktop = not self.is_mobile
```

### **Color-Coded Danger Levels:**

- **High (8-10):** Red background
- **Medium (5-7):** Orange background
- **Low (1-4):** Green background

## 🔧 Development Workflow

1. **Setup Environment:**

   - Install Kivy: `pip install kivy`
   - Install dependencies: `pip install plyer`

2. **Development:**

   - Edit logic in Python files
   - Style in KV files (recommended)
   - Test on desktop first

3. **Android Build:**

   - Configure `buildozer.spec`
   - Run `buildozer android debug`

## 🎉 Success Metrics

# Food Allergy Database (Kivy)

This is a small cross-platform Kivy application that stores food allergies in a local SQLite database, lets you rate the danger level, and search ingredients.

This repository contains:

- `allergy_database.py` — application logic, database manager, and Kivy App class
- `allergydatabase.kv` — KV layout file (single source of truth for the UI)
- `buildozer.spec` — Android packaging configuration (for use with Buildozer / python-for-android)
- `icon.png`, `presplash.png` — placeholder images (generated by `tools/generate_placeholders.py`). Replace with production assets as needed

## Quick start — run on Windows

Requirements:

- Python 3.10+ (3.13 was used during development)
- Kivy 2.3.1 (pinned in `buildozer.spec` and recommended for parity)

Install dependencies (recommended in a virtualenv):

```powershell
python -m pip install kivy==2.3.1
```

Run the app:

```powershell
python allergy_database.py
```

The app will create `allergies.db` in the working directory on first run.

## App features

- Add new allergy entries with name, danger level (1–4), symptoms, ingredients, and notes
- List all allergies ordered by danger level
- Search by allergen name or ingredients (case-insensitive substring match)
- Delete entries with confirmation

UI details:

- The UI is defined in `allergydatabase.kv` to avoid duplication and keep layout portable between desktop and mobile
- `UIConfig` in `allergy_database.py` detects the platform and sets larger touch targets on mobile

## Android build (local)

This project is prepared for packaging with Buildozer (Linux/WSL or macOS required for android builds). The repo already includes a `buildozer.spec` with pinned Kivy and placeholder assets.

Basic local steps (on WSL or a Linux machine):

```bash
# install buildozer & dependencies (on Debian/Ubuntu)
sudo apt update && sudo apt install -y build-essential git python3-pip python3-virtualenv
pip install --user buildozer

# in repo root
buildozer android debug
```

Notes:

- `buildozer.spec` expects `icon.png` and `presplash.png` at the repo root (these are present as placeholders). If you move or rename them, update `icon.filename` and `presplash.filename` in `buildozer.spec`
- For a Play Store release, you will need a Java keystore for signing. CI in this project decodes a base64 keystore secret; locally you can set `android.release_keystore`, `android.release_keyalias`, and the passwords in `buildozer.spec` (or provide them via environment)

## Placeholder images

A small helper script generates the example images used in this repo:

```powershell
python tools/generate_placeholders.py
```

It will create `icon.png` (512×512) and `presplash.png` (2732×2732) at the repo root. Replace them with your finalized artwork before releasing.

## Troubleshooting

- If the app fails to start on Windows, ensure Kivy is installed and your Python version is compatible. Check the console for tracebacks
- If screens show duplicated widgets, ensure the KV file `allergydatabase.kv` is present and the app is started from the repository root so Kivy can load the KV file automatically
- For Android build failures, run Buildozer in verbose mode (`buildozer -v android debug`) and read the log for missing recipes or dependency issues

## Developer notes

- Architecture: KV-first UI (presentation) + Python controllers (logic) in `allergy_database.py`
- Database: SQLite file `allergies.db` created in working directory
- Popup auto-dismiss timeout is configurable via `UIConfig.success_popup_timeout` in `allergy_database.py`

If you'd like, I can add:

- Play Store publishing steps in the CI workflow (requires Play Console service account keys)
- additional image sizes and `res/` folder layout for Android
- automated unit tests for the database layer

---

Generated on 2025-09-21
