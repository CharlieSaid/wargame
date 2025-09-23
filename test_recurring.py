# This script is used to test if the service is able to regularly execute the recruit.py and battle.py scripts.
# It's a simple test that logs execution times to verify scheduling is working.

import time
import os
from datetime import datetime

def main():
    """Test script to verify scheduling is working"""
    print("Test recurring script started")
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Log to both console and file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"Test script executed at {timestamp}"
    
    print(log_message)
    
    # Write to log file
    with open("logs/test_recurring.log", "a") as log_file:
        log_file.write(log_message + "\n")
    
    print("Test recurring script completed")

if __name__ == "__main__":
    main()
