# Post-build script to copy necessary DLLs for Kivy Briefcase packaging
# This script should be run after 'briefcase build' to ensure all required DLLs are in place

param(
    [string]$BuildPath = ""
)

Write-Host "Starting post-build DLL copy process..." -ForegroundColor Green

# Determine build directory
if ($BuildPath -eq "") {
    $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
    $BuildDir = Join-Path $ScriptDir "..\build\foodallergyshield\windows\app\src"
} else {
    $BuildDir = $BuildPath
}

$BuildDir = Resolve-Path $BuildDir -ErrorAction SilentlyContinue

# Check if build directory exists
if (-not $BuildDir -or -not (Test-Path $BuildDir)) {
    Write-Host "Error: Build directory not found at $BuildDir" -ForegroundColor Red
    Write-Host "Please run 'briefcase build' first." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Build directory found: $BuildDir" -ForegroundColor Cyan

# Change to the build directory
Set-Location $BuildDir

# Function to copy DLLs with error handling
function Copy-DLLs {
    param(
        [string]$SourcePath,
        [string]$Description,
        [string]$Pattern = "*.dll"
    )
    
    Write-Host "Copying $Description..." -ForegroundColor Yellow
    
    if (Test-Path $SourcePath) {
        $SourceFiles = Join-Path $SourcePath $Pattern
        try {
            Copy-Item $SourceFiles -Destination . -Force -ErrorAction Stop
            Write-Host "- $Description copied successfully" -ForegroundColor Green
        } catch {
            Write-Host "Warning: Failed to copy $Description - $_" -ForegroundColor Red
        }
    } else {
        Write-Host "Warning: $Description not found at $SourcePath" -ForegroundColor Red
    }
}

# Copy SDL2 DLLs
Copy-DLLs -SourcePath "app_packages\share\sdl2\bin" -Description "SDL2 DLLs"

# Copy GLEW DLLs
Copy-DLLs -SourcePath "app_packages\share\glew\bin" -Description "GLEW DLL" -Pattern "glew32.dll"

# Copy ANGLE DLLs
Copy-DLLs -SourcePath "app_packages\share\angle\bin" -Description "ANGLE DLLs"

Write-Host ""
Write-Host "Post-build DLL copy process completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Your application executable is ready at:" -ForegroundColor Cyan
Write-Host "$BuildDir\Food Allergy Shield.exe" -ForegroundColor White
Write-Host ""
Write-Host "You can now run the application or distribute the entire src folder." -ForegroundColor Yellow

# List copied DLLs for verification
Write-Host ""
Write-Host "Copied DLL files:" -ForegroundColor Cyan
Get-ChildItem -Path . -Filter "*.dll" | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize

Read-Host "Press Enter to exit"