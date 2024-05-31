import sys
import os
import unittest
from rich.console import Console

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import config
from modules.core.username import verifyUsername
from modules.core.email import verifyEmail
from modules.export.csv import saveToCsv
from modules.export.pdf import saveToPdf
from modules.utils.userAgent import getRandomUserAgent
from datetime import datetime
from modules.whatsmyname.list_operations import checkUpdates

config.no_nsfw = None
config.proxy = None
config.verbose = None
config.timeout = None
config.dump = True
config.csv = None
config.pdf = None
config.filter = "name=Gravatar"
config.console = Console()
config.userAgent = getRandomUserAgent()

config.dateRaw = datetime.now().strftime("%m_%d_%Y")
config.datePretty = datetime.now().strftime("%B %d, %Y")

checkUpdates()


class TestEmail(unittest.TestCase):
    config.currentEmail = "john@gmail.com"

    def test_verify_email(self):

        result = verifyEmail(config.currentEmail)
        self.assertTrue(result)


class TestUsername(unittest.TestCase):
    config.currentUser = "p1ngul1n0"

    def test_verify_username(self):
        result = verifyUsername(config.currentUser)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
