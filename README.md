# Food Allergy Shield

![Food Safety](img/all_allergies.png)

A simple cross-platform application for managing food allergy information, built with Kivy.

## 🏗️ Project Structure

```
FoodAllergyShield/
├── src/                           # Source code
│   └── foodallergyshield/        # Main application package
│       ├── __init__.py           # Package initialization
│       ├── __main__.py           # CLI entry point
│       ├── app.py                # Briefcase entry point
│       ├── food_allergy_shield.py # Main application logic
│       ├── database_manager.py   # Database operations
│       └── food_allergy_shield.kv # UI layout (Kivy)
├── assets/                       # Static assets
│   ├── icon.ico                  # Application icon (Windows)
│   ├── presplash.png            # Splash screen image
│   └── img/                     # Other images
├── data/                        # Data files
│   ├── food_allergies.db        # SQLite database
│   ├── food_allergies_export.csv # Sample export
│   └── sample_data.csv          # Sample data
├── docs/                        # Documentation
├── archive/                     # Archived original files
├── build/                       # Briefcase build output
├── dist/                        # Distribution packages
├── logs/                        # Application logs
├── tools/                       # Development tools
├── run_dev.py                   # Development runner (Python)
├── run_dev.bat                  # Development runner (Windows)
├── run_dev.sh                   # Development runner (Unix/Linux)
├── pyproject.toml              # Project configuration (Briefcase)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Development Mode

**Windows:**
```bash
# Double-click or run:
run_dev.bat
```

**Python (all platforms):**
```bash
python run_dev.py
```

**Unix/Linux/macOS:**
```bash
chmod +x run_dev.sh
./run_dev.sh
```

### Packaging with Briefcase

```bash
# Development testing
briefcase dev

# Create/update build
briefcase create
briefcase update

# Build executable
briefcase build

# Create installer package
briefcase package
```

## 📋 Requirements

- Python 3.8+
- Kivy 2.3.0+
- Briefcase (for packaging)

Install dependencies:
```bash
pip install -r requirements.txt
pip install briefcase  # For packaging
```

## 🔧 Development

### Making Changes

1. Edit files in `src/foodallergyshield/`
2. Test with `python run_dev.py` (automatically copies database from `data/`)
3. For packaging: `briefcase update && briefcase build`

### Database Management

- **Development**: Database automatically copied from `data/food_allergies.db` to `src/foodallergyshield/` when running development scripts
- **Distribution**: Database (`food_allergies.db`) is included in the MSI package
- **Data Directory**: Sample data and main database stored in `data/`

### File Structure Guidelines

- **Source Code**: All Python code goes in `src/foodallergyshield/`
- **Assets**: Images, icons in `assets/`
- **Data**: Database files, CSV data in `data/`
- **Documentation**: Markdown files in `docs/`

### Key Files

- `src/foodallergyshield/food_allergy_shield.py` - Main application logic
- `src/foodallergyshield/database_manager.py` - Database operations
- `src/foodallergyshield/food_allergy_shield.kv` - UI layout
- `pyproject.toml` - Briefcase configuration

## 📦 Distribution

The project creates:
- **Windows**: `Food Allergy Shield-1.0.0.msi` installer
- **Executable**: `Food Allergy Shield.exe` standalone

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're running from project root
2. **KV file not found**: Check that `.kv` file is in `src/foodallergyshield/`
3. **Database errors**: Ensure `data/` directory exists

### Development vs Production

- **Development**: Use `run_dev.py` for quick testing
- **Production**: Use `briefcase build` for final executable

## 📄 License

MIT License - see LICENSE file for details.

## 👥 Contributing

1. Make changes in `src/foodallergyshield/`
2. Test with development scripts
3. Update documentation if needed
4. Create pull request