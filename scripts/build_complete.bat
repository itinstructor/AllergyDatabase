@echo off
REM Complete build script for Food Allergy Shield
REM This script builds the application and copies all necessary DLLs

echo ========================================
echo Food Allergy Shield - Complete Build
echo ========================================
echo.

REM Check if we're in the correct directory
if not exist "pyproject.toml" (
    echo Error: pyproject.toml not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

echo Step 1: Cleaning previous build...
echo.
if exist "%~dp0..\build" (
    echo Removing existing build directory...
    rmdir /s /q "%~dp0..\build"
    echo - Build directory removed successfully
) else (
    echo - No existing build directory found
)

echo.
echo Step 2: Building application with Briefcase...
echo.
briefcase build

if %errorlevel% neq 0 (
    echo.
    echo Error: Briefcase build failed!
    pause
    exit /b %errorlevel%
)

echo.
echo Step 3: Copying necessary DLLs...
echo.

REM Set the build directory
set BUILD_DIR=%~dp0..\build\foodallergyshield\windows\app\src

REM Check if build directory exists
if not exist "%BUILD_DIR%" (
    echo Error: Build directory not found. Build may have failed.
    pause
    exit /b 1
)

REM Change to the build directory
cd /d "%BUILD_DIR%"

REM Copy SDL2 DLLs
echo Copying SDL2 DLLs...
if exist "app_packages\share\sdl2\bin\*.dll" (
    copy "app_packages\share\sdl2\bin\*.dll" . >nul 2>&1
    echo - SDL2 DLLs copied successfully
) else (
    echo Warning: SDL2 DLLs not found
)

REM Copy GLEW DLLs
echo Copying GLEW DLLs...
if exist "app_packages\share\glew\bin\glew32.dll" (
    copy "app_packages\share\glew\bin\glew32.dll" . >nul 2>&1
    echo - GLEW DLL copied successfully
) else (
    echo Warning: GLEW DLL not found
)

REM Copy ANGLE DLLs
echo Copying ANGLE DLLs...
if exist "app_packages\share\angle\bin\*.dll" (
    copy "app_packages\share\angle\bin\*.dll" . >nul 2>&1
    echo - ANGLE DLLs copied successfully
) else (
    echo Warning: ANGLE DLLs not found
)

echo.
echo ========================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Your application is ready at:
echo %BUILD_DIR%\Food Allergy Shield.exe
echo.
echo To test the application, you can run:
echo briefcase run
echo.
echo Or navigate to the build directory and run the executable directly.
echo.
pause