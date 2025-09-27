# Build Scripts for Food Allergy Shield

This directory contains automated build scripts to help with packaging the Food Allergy Shield application using Briefcase.

## Scripts Overview

### Complete Build Scripts (Recommended)

These scripts perform both the Briefcase build and the necessary DLL copying in one step:

- **`build_complete.bat`** - Windows batch script for complete build process
- **`build_complete.ps1`** - PowerShell script for complete build process (more detailed output)

### Post-Build Scripts

These scripts only copy the necessary DLLs after you've already run `briefcase build`:

- **`post_build.bat`** - Windows batch script for DLL copying only
- **`post_build.ps1`** - PowerShell script for DLL copying only (more detailed output)
- **`post_build.sh`** - Bash script for Linux/macOS/WSL environments

## Usage Instructions

### Option 1: Complete Build (Recommended)

#### Windows Command Prompt / PowerShell:

```cmd
# From the project root directory
scripts\build_complete.bat
```

#### PowerShell (for detailed output):

```powershell
# From the project root directory
.\scripts\build_complete.ps1
```

### Option 2: Manual Build + Post-Build

#### Step 1: Build with Briefcase

```cmd
briefcase build
```

#### Step 2: Copy DLLs

```cmd
# Windows Command Prompt
scripts\post_build.bat

# PowerShell
.\scripts\post_build.ps1

# Linux/macOS/WSL
./scripts/post_build.sh
```

## What These Scripts Do

### Complete Build Scripts (`build_complete.*`)

1. **Clean Build**: Remove any existing build directory for a fresh start
2. **Build Process**: Run `briefcase build` to create the Windows executable
3. **DLL Copying**: Automatically copy necessary DLLs to the executable directory

### Post-Build Scripts (`post_build.*`)

1. **DLL Copying Only**: Copy necessary DLLs to the executable directory:
   - **SDL2 DLLs**: SDL2.dll, SDL2_image.dll, SDL2_mixer.dll, SDL2_ttf.dll
   - **GLEW DLL**: glew32.dll
   - **ANGLE DLLs**: libEGL.dll, libGLESv2.dll, d3dcompiler_47.dll

## Why These Scripts Are Needed

Briefcase packages Kivy applications with all dependencies, but the necessary DLL files are placed deep in the `app_packages` directory structure. The Windows executable can't find them at runtime, causing errors like:

- `ImportError: DLL load failed while importing _window_sdl2`
- `AttributeError: 'NoneType' object has no attribute 'size'`

These scripts solve this by copying the DLLs to the same directory as the executable, where Windows can find them.

## Output Location

After running the scripts, your application will be ready at:

```bash
build\foodallergyshield\windows\app\src\Food Allergy Shield.exe
```

You can distribute the entire `src` folder, which contains the executable and all necessary DLL files.

## Testing the Application

After building, you can test the application with:

```cmd
briefcase run
```

Or navigate to the build directory and run the executable directly.

## Troubleshooting

- **Script not found**: Make sure you're running the script from the project root directory
- **Permission denied**: On PowerShell, you may need to adjust execution policy:
  
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- **Build fails**: Ensure all dependencies are installed and you have the latest version of Briefcase
- **DLLs not copied**: Check that the build completed successfully before running post-build scripts