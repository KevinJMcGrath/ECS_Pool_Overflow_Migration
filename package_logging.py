import logging.handlers
import sys

import config

# Log Filter class
class LogFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.__level = level

    def filter(self, log_record):
        return log_record.levelno <= self.__level


# Define the root logging instance
root_logger = logging.getLogger()

if config.LogVerbose:
    print(f'Verbose logging is on.')
    root_logger.setLevel(logging.DEBUG)
else:
    print(f'Verbose logging is off.')
    root_logger.setLevel(logging.INFO)



# Log Formatting
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
formatter.datefmt = '%m/%d %H:%M:%S'



def initialize_logging():
    def set_handler_type(stream=sys.stdout):
        return logging.StreamHandler(stream)

    # Somewhere I managed to add a call to a logging statement that gets run before I initialize the
    # logging system. When that happens, I need to make sure I purge the old default handler or
    # I'll get double entries.
    if root_logger.hasHandlers():
        print('Removing default handler...')
        h = root_logger.handlers[0]
        root_logger.removeHandler(h)


    # Define the logging handlers
    if config.LogVerbose:
        debug_handler = set_handler_type()
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)
        debug_handler.addFilter(LogFilter(logging.DEBUG))
        root_logger.addHandler(debug_handler)

    info_handler = set_handler_type()
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    info_handler.addFilter(LogFilter(logging.INFO))
    root_logger.addHandler(info_handler)

    warn_handler = set_handler_type()
    warn_handler.setLevel(logging.WARNING)
    warn_handler.setFormatter(formatter)
    warn_handler.addFilter(LogFilter(logging.WARNING))
    root_logger.addHandler(warn_handler)

    error_handler = set_handler_type(stream=sys.stderr)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    error_handler.addFilter(LogFilter(logging.ERROR))
    root_logger.addHandler(error_handler)





