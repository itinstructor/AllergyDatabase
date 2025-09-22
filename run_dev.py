#!/usr/bin/env python3
"""
Development runner for Food Allergy Shield

This script allows you to run the app directly from the project root
during development, using the source code in src/foodallergyshield/
"""

import sys
import os
import shutil
from pathlib import Path

# Add the src directory to Python path
project_root = Path(__file__).parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

# Ensure database file is available in the src directory for development
data_db = project_root / "data" / "food_allergies.db"
src_db = src_dir / "foodallergyshield" / "food_allergies.db"

if data_db.exists() and (not src_db.exists() or data_db.stat().st_mtime > src_db.stat().st_mtime):
    print(f"📋 Copying database from {data_db} to {src_db}")
    shutil.copy2(data_db, src_db)

# Change to src directory so relative imports work
os.chdir(src_dir / "foodallergyshield")

try:
    from foodallergyshield.food_allergy_shield import AllergyDatabaseApp
    
    if __name__ == "__main__":
        print("🚀 Starting Food Allergy Shield in development mode...")
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"🐍 Python path includes: {src_dir}")
        print("=" * 50)
        
        app = AllergyDatabaseApp()
        app.run()
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure you're running this from the project root directory")
    print("💡 Check that src/foodallergyshield/ contains all required files")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting application: {e}")
    sys.exit(1)