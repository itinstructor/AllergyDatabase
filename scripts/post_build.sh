#!/bin/bash
# Post-build script to copy necessary DLLs for Kivy Briefcase packaging
# This script can be used on Linux/macOS or Windows with WSL/Git Bash

echo "Starting post-build DLL copy process..."

# Determine script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/../build/foodallergyshield/windows/app/src"

# Check if build directory exists
if [ ! -d "$BUILD_DIR" ]; then
    echo "Error: Build directory not found at $BUILD_DIR"
    echo "Please run 'briefcase build' first."
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Build directory found: $BUILD_DIR"

# Change to the build directory
cd "$BUILD_DIR" || exit 1

# Function to copy files with error handling
copy_dlls() {
    local source_path="$1"
    local description="$2"
    local pattern="${3:-*.dll}"
    
    echo "Copying $description..."
    
    if [ -d "$source_path" ]; then
        if cp "$source_path"/$pattern . 2>/dev/null; then
            echo "- $description copied successfully"
        else
            echo "Warning: Failed to copy $description"
        fi
    else
        echo "Warning: $description not found at $source_path"
    fi
}

# Copy SDL2 DLLs
copy_dlls "app_packages/share/sdl2/bin" "SDL2 DLLs"

# Copy GLEW DLLs
copy_dlls "app_packages/share/glew/bin" "GLEW DLL" "glew32.dll"

# Copy ANGLE DLLs
copy_dlls "app_packages/share/angle/bin" "ANGLE DLLs"

echo ""
echo "Post-build DLL copy process completed!"
echo ""
echo "Your application executable is ready at:"
echo "$BUILD_DIR/Food Allergy Shield.exe"
echo ""
echo "You can now run the application or distribute the entire src folder."

# List copied DLLs for verification
echo ""
echo "Copied DLL files:"
ls -la *.dll 2>/dev/null || echo "No DLL files found"

read -p "Press Enter to exit..."