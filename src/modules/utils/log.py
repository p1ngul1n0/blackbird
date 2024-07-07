import logging


def logError(e, message, config):
    if str(e) != "":
        error = str(e)
    else:
        error = repr(e)
    logging.error(f"{message} | {error}")
    if config.verbose:
        config.console.print(f"⛔  {message}")
        config.console.print("     | An error occurred:")
        config.console.print(f"     | {error}")
