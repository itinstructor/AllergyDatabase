@echo off
REM Post-build script to copy necessary DLLs for Kivy Briefcase packaging
REM This script should be run after 'briefcase build' to ensure all required DLLs are in place

echo Starting post-build DLL copy process...

REM Set the build directory
set BUILD_DIR=%~dp0..\build\foodallergyshield\windows\app\src

REM Check if build directory exists
if not exist "%BUILD_DIR%" (
    echo Error: Build directory not found at %BUILD_DIR%
    echo Please run 'briefcase build' first.
    pause
    exit /b 1
)

echo Build directory found: %BUILD_DIR%

REM Change to the build directory
cd /d "%BUILD_DIR%"

REM Copy SDL2 DLLs
echo Copying SDL2 DLLs...
if exist "app_packages\share\sdl2\bin\*.dll" (
    copy "app_packages\share\sdl2\bin\*.dll" . >nul
    echo - SDL2 DLLs copied successfully
) else (
    echo Warning: SDL2 DLLs not found in app_packages\share\sdl2\bin\
)

REM Copy GLEW DLLs
echo Copying GLEW DLLs...
if exist "app_packages\share\glew\bin\glew32.dll" (
    copy "app_packages\share\glew\bin\glew32.dll" . >nul
    echo - GLEW DLL copied successfully
) else (
    echo Warning: GLEW DLL not found in app_packages\share\glew\bin\
)

REM Copy ANGLE DLLs
echo Copying ANGLE DLLs...
if exist "app_packages\share\angle\bin\*.dll" (
    copy "app_packages\share\angle\bin\*.dll" . >nul
    echo - ANGLE DLLs copied successfully
) else (
    echo Warning: ANGLE DLLs not found in app_packages\share\angle\bin\
)

echo.
echo Post-build DLL copy process completed!
echo.
echo Your application executable is ready at:
echo %BUILD_DIR%\Food Allergy Shield.exe
echo.
echo You can now run the application or distribute the entire src folder.
pause