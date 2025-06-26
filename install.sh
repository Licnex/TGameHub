#!/bin/bash
# TGameHub Installation Script for Linux/macOS
# This script will install all required dependencies for TGameHub

echo ""
echo "========================================"
echo " TGameHub Installation Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        echo "Please install Python 3.7+ from your package manager or https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python found!"
$PYTHON_CMD --version

echo ""
echo "Installing required packages..."
echo ""

# Upgrade pip first
echo "Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip

# Install requirements
echo "Installing TGameHub dependencies..."
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Some packages failed to install automatically."
    echo "Trying individual installation..."
    echo ""
    
    echo "Installing numpy..."
    $PYTHON_CMD -m pip install numpy
    
    echo "Installing chess..."
    $PYTHON_CMD -m pip install chess
    
    echo "Installing colorama..."
    $PYTHON_CMD -m pip install colorama
fi

echo ""
echo "========================================"
echo " Installation Complete!"
echo "========================================"
echo ""
echo "To run TGameHub, use:"
echo "   $PYTHON_CMD Main.py"
echo ""
echo "If you encounter any issues:"
echo "1. Make sure your terminal window is large"
echo "2. Try zooming out your terminal"
echo "3. Check GitHub issues: github.com/Licnex/tgamehub"
echo ""
