#!/bin/bash

# Exit script if any command fails
set -e

screen -S lolo

VENV_DIR="/home/ec2-user/Lolo-Botsado/venv"

source "$VENV_DIR/bin/activate"

cd /home/ec2-user/Lolo-Botsado

python oldbot.py