#!/bin/bash

# Define the log file path
LOG_FILE="/home/ec2-user/Lolo-Botsado/scriptLogs/before_install_log.log"

# Create or append to the log file
echo "Running stop_bot_screen.sh at $(date)" >> "$LOG_FILE"

# Find and kill the screen session named 'lolo'
screen -ls | grep "lolo" | cut -d. -f1 | tr --delete "\t" | xargs kill -9 >> "$LOG_FILE" 2>&1

# Clean up dead screen sessions
screen -wipe >> "$LOG_FILE" 2>&1

# List remaining screen sessions (for debugging/logging purposes)
screen -ls >> "$LOG_FILE" 2>&1

# Log script completion
echo "Script completed at $(date)" >> "$LOG_FILE"
