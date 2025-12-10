#!/bin/bash

# Script to install dependencies and set up Python virtual environment
# Usage: ./install_deps.sh

set -e  # Exit on error

VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"

echo "=== Dependency Installer ==="

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "Error: $REQUIREMENTS_FILE not found in current directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment '$VENV_DIR' not found. Creating..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created."
else
    echo "Virtual environment '$VENV_DIR' already exists."
fi

# Determine activation script based on OS
if [ -f "$VENV_DIR/bin/activate" ]; then
    ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
elif [ -f "$VENV_DIR/Scripts/activate" ]; then
    ACTIVATE_SCRIPT="$VENV_DIR/Scripts/activate"
else
    echo "Error: Could not find activate script in $VENV_DIR."
    exit 1
fi

echo "Activating virtual environment..."
# shellcheck disable=SC1090
source "$ACTIVATE_SCRIPT"

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies from $REQUIREMENTS_FILE..."
pip install -r "$REQUIREMENTS_FILE"

echo "=== Installation completed successfully ==="
echo "To activate the virtual environment manually, run:"
echo -e "\033[33m  source $ACTIVATE_SCRIPT\033[0m"