# Development Guide

## Project Structure Overview

This project now uses a clean, modern Python project structure following current best practices.

### Directory Layout

- **`src/foodallergyshield/`** - Main source code (single source of truth)
- **`assets/`** - Static files (icons, images)
- **`data/`** - Database and data files
- **`docs/`** - Documentation files
- **`archive/`** - Archived original files (for reference)

### Development Workflow

1. **Edit source code** in `src/foodallergyshield/`
2. **Test quickly** with `python run_dev.py`
3. **Package for distribution** with Briefcase commands

### Running the Application

#### Quick Development Testing
```python
# From project root:
python run_dev.py
```

#### Briefcase Development Mode
```bash
briefcase dev
```

#### Building for Distribution
```bash
briefcase create    # First time setup
briefcase update    # After code changes
briefcase build     # Create executable
briefcase package   # Create installer
```

### File Organization

All active development happens in `src/foodallergyshield/`:
- `food_allergy_shield.py` - Main app logic and UI screens
- `database_manager.py` - Database operations
- `food_allergy_shield.kv` - Kivy UI layout
- `app.py` - Entry point for Briefcase packaging

The root directory contains only:
- Configuration files (`pyproject.toml`, `requirements.txt`)
- Development scripts (`run_dev.*`)
- Asset and data directories
- Documentation

### Benefits of This Structure

✅ **Clean separation** between source code and assets
✅ **Modern Python standards** (src/ layout)
✅ **Briefcase-native** packaging
✅ **Single source of truth** - no duplicate files
✅ **Easy development** with simple run scripts

### Making Changes

1. Edit files in `src/foodallergyshield/`
2. Test with `python run_dev.py`
3. When ready to package: `briefcase update && briefcase build`
4. Create installer: `briefcase package`

### Troubleshooting

- **Import errors**: Ensure you're running from project root
- **Missing files**: Check that all files are in `src/foodallergyshield/`
- **Build issues**: Try `briefcase create --no-input` to regenerate