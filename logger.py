import logging

# Configure the logger to write to 'app.log'
logging.basicConfig(
    filename='app.log',
    level=logging.INFO, # Set the minimum logging level to capture
    format='%(asctime)s - %(levelname)s - %(message)s' # Define the message format
)

# Log some messages
logging.debug('This is a debug message (will be ignored by default)')
logging.info('This is an informational message')
logging.warning('This is a warning message')
logging.error('This is an error message')
