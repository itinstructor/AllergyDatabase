# Complete build script for Food Allergy Shield
# This script builds the application and copies all necessary DLLs

Write-Host "========================================" -ForegroundColor Green
Write-Host "Food Allergy Shield - Complete Build" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if we're in the correct directory
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "Error: pyproject.toml not found. Please run this script from the project root directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Step 1: Cleaning previous build..." -ForegroundColor Yellow
Write-Host ""

# Remove existing build directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BuildRootDir = Join-Path $ScriptDir "..\build"

if (Test-Path $BuildRootDir) {
    Write-Host "Removing existing build directory..." -ForegroundColor Cyan
    try {
        Remove-Item -Recurse -Force $BuildRootDir -ErrorAction Stop
        Write-Host "- Build directory removed successfully" -ForegroundColor Green
    } catch {
        Write-Host "Warning: Failed to remove build directory - $_" -ForegroundColor Red
    }
} else {
    Write-Host "- No existing build directory found" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Building application with Briefcase..." -ForegroundColor Yellow
Write-Host ""

# Run briefcase build
$buildResult = Start-Process -FilePath "briefcase" -ArgumentList "build" -Wait -PassThru -NoNewWindow

if ($buildResult.ExitCode -ne 0) {
    Write-Host ""
    Write-Host "Error: Briefcase build failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit $buildResult.ExitCode
}

Write-Host ""
Write-Host "Step 3: Copying necessary DLLs..." -ForegroundColor Yellow
Write-Host ""

# Set the build directory
$BuildDir = Join-Path $ScriptDir "..\build\foodallergyshield\windows\app\src"
$BuildDir = Resolve-Path $BuildDir -ErrorAction SilentlyContinue

# Check if build directory exists
if (-not $BuildDir -or -not (Test-Path $BuildDir)) {
    Write-Host "Error: Build directory not found. Build may have failed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Change to the build directory
Set-Location $BuildDir

# Function to copy DLLs with error handling
function Copy-DLLs {
    param(
        [string]$SourcePath,
        [string]$Description,
        [string]$Pattern = "*.dll"
    )
    
    Write-Host "Copying $Description..." -ForegroundColor Cyan
    
    if (Test-Path $SourcePath) {
        $SourceFiles = Join-Path $SourcePath $Pattern
        try {
            Copy-Item $SourceFiles -Destination . -Force -ErrorAction Stop
            Write-Host "- $Description copied successfully" -ForegroundColor Green
        } catch {
            Write-Host "Warning: Failed to copy $Description" -ForegroundColor Red
        }
    } else {
        Write-Host "Warning: $Description not found" -ForegroundColor Red
    }
}

# Copy DLLs
Copy-DLLs -SourcePath "app_packages\share\sdl2\bin" -Description "SDL2 DLLs"
Copy-DLLs -SourcePath "app_packages\share\glew\bin" -Description "GLEW DLL" -Pattern "glew32.dll"
Copy-DLLs -SourcePath "app_packages\share\angle\bin" -Description "ANGLE DLLs"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "BUILD COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your application is ready at:" -ForegroundColor Cyan
Write-Host "$BuildDir\Food Allergy Shield.exe" -ForegroundColor White
Write-Host ""
Write-Host "To test the application, you can run:" -ForegroundColor Yellow
Write-Host "briefcase run" -ForegroundColor White
Write-Host ""
Write-Host "Or navigate to the build directory and run the executable directly." -ForegroundColor Yellow
Write-Host ""

# List final DLL files for verification
Write-Host "Final DLL inventory:" -ForegroundColor Cyan
Get-ChildItem -Path . -Filter "*.dll" | Select-Object Name, @{Name="Size (KB)"; Expression={[math]::Round($_.Length/1KB,1)}} | Format-Table -AutoSize

Read-Host "Press Enter to exit"