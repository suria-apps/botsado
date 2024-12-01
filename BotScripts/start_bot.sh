#!/bin/bash

# Exit script if any command fails
set -e

# Define the virtual environment directory and application directory
VENV_DIR="/home/ec2-user/Lolo-Botsado/venv"
APP_DIR="/home/ec2-user/Lolo-Botsado"
APP_SCRIPT="oldbot.py"

# Start a screen session and run commands in it
screen -dmS lolo bash -c "
    # Activate the virtual environment
    source \"$VENV_DIR/bin/activate\" &&
    # Navigate to the application directory
    cd \"$APP_DIR\" &&
    # Start the Python application
    python \"$APP_SCRIPT\" &&
    # Keep the screen session open (optional for debugging)
    exec bash
"
