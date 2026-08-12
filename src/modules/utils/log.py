import logging
import traceback

def logError(e, message, config):
    if str(e) != "":
        error = str(e)
    else:
        error = repr(e)
    stacktrace = traceback.format_exc()
    
    logging.error(f"{message} | {error}")
    logging.error(stacktrace)
    if config.verbose:
        config.console.print(f"⛔  {message}")
        config.console.print("     | An error occurred:")
        config.console.print(f"     | {error}")
