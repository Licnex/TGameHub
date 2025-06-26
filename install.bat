@echo off
REM TGameHub Installation Script for Windows
REM This script will install all required dependencies for TGameHub

echo.
echo ========================================
echo  TGameHub Installation Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
python --version

echo.
echo Installing required packages...
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing TGameHub dependencies...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo WARNING: Some packages failed to install automatically.
    echo Trying individual installation...
    echo.
    
    echo Installing numpy...
    python -m pip install numpy
    
    echo Installing chess...
    python -m pip install chess
    
    echo Installing windows-curses for Windows...
    python -m pip install windows-curses
    
    echo Installing colorama...
    python -m pip install colorama
)

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo To run TGameHub, use:
echo   python Main.py
echo.
echo If you encounter any issues:
echo 1. Make sure your terminal window is large
echo 2. Try zooming out your terminal
echo 3. Check GitHub issues: github.com/Licnex/tgamehub
echo.
pause
