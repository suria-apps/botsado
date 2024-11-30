#!/bin/bash

# Exit script if any command fails
set -e

# Define log file path
LOG_FILE="/home/ec2-user/Lolo-Botsado/install_dependencies.log"

# Redirect all output (stdout and stderr) to the log file
exec > >(tee -a "$LOG_FILE") 2>&1

echo "===== Starting Dependency Installation ====="
date

# Define the path to your virtual environment
VENV_DIR="/home/ec2-user/Lolo-Botsado/venv"

# Define the path to the requirements.txt file
REQUIREMENTS_FILE="/home/ec2-user/Lolo-Botsado/requirements.txt"

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "Error: $REQUIREMENTS_FILE not found!"
    exit 1
fi

# Deactivate the virtual environment
deactivate

echo "Dependencies installed successfully!"
date
echo "===== Dependency Installation Completed ====="
