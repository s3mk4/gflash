@echo off
REM gFlash v0.3.2 - Build script for Windows

echo [*] gFlash Builder v0.3.2
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.7+ first.
    pause
    exit /b 1
)

echo [*] Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [*] Building executables...
python build.py

if errorlevel 1 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)

echo.
echo [OK] Build complete! Check dist/ folder
echo.
pause
