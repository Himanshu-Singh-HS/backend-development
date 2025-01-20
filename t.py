import os
import logging

# Define the path for the log file
log_file = os.path.join(os.path.dirname(__file__), 'test_log.log')

# Print the path to ensure it's correct
print(f"Log file path: {log_file}")

# Set up logging to both file and console
logging.basicConfig(
    level=logging.INFO,  # Set log level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),  # Log to the file
        logging.StreamHandler()         # Log to the console
    ]
)

# Test log messages
logging.info("This is an INFO log entry.")
logging.debug("This is a DEBUG log entry.")  # Won't appear because level is INFO
logging.warning("This is a WARNING log entry.")
logging.error("This is an ERROR log entry.")
logging.critical("This is a CRITICAL log entry.")

# Add a message to indicate logging is done
print("Logging complete. Check the 'test_log.log' file.")

# Explicitly shut down the logging system to flush logs to the file
logging.shutdown()

