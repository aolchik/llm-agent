# logger_config.py

import logging

# Configure the root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a common logger instance
logger = logging.getLogger('tool-evaluator-agent')

# Example: Adding a file handler
file_handler = logging.FileHandler('logs/app-debug.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - '
                      '%(levelname)s - %(message)s'))
logger.addHandler(file_handler)
