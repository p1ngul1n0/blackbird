import random
import os


def getRandomUserAgent(config):
    path = os.path.join(
        os.path.join(os.path.dirname(__file__)),
        "..",
        "..",
        "..",
        "data",
        "useragents.txt",
    )
    userAgents = open(path).read().splitlines()
    userAgent = random.choice(userAgents)
    if config.verbose:
        config.console.print(f':id: Selected random User-Agent "{userAgent}"')
    return userAgent
