@echo off
REM Windows batch script for running Food Allergy Shield in development mode

echo 🚀 Starting Food Allergy Shield in development mode...
echo.

REM Check if we're in the right directory
if not exist "src\foodallergyshield\food_allergy_shield.py" (
    echo ❌ Error: Cannot find src\foodallergyshield\food_allergy_shield.py
    echo 💡 Make sure you're running this from the project root directory
    pause
    exit /b 1
)

REM Copy database if needed
if exist "data\food_allergies.db" (
    if not exist "src\foodallergyshield\food_allergies.db" (
        echo 📋 Copying database for development...
        copy "data\food_allergies.db" "src\foodallergyshield\food_allergies.db" >nul
    )
)

REM Run the development script
python run_dev.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo ❌ Application exited with an error
    pause
)