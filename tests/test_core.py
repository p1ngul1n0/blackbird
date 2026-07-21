import sys
import os
import asyncio
import unittest
from unittest.mock import AsyncMock, Mock, patch
from rich.console import Console

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import config
from src.modules.core.username import verifyUsername
from src.modules.core.email import checkSite, verifyEmail
from src.modules.export.csv import saveToCsv
from src.modules.export.pdf import saveToPdf
from src.modules.utils.userAgent import getRandomUserAgent
from datetime import datetime
from src.modules.whatsmyname.list_operations import checkUpdates

config.no_nsfw = None
config.proxy = None
config.verbose = None
config.timeout = None
config.dump = True
config.csv = None
config.pdf = None
config.filter = "name=Gravatar"
config.console = Console()
config.userAgent = getRandomUserAgent(config)
config.max_concurrent_requests = 30

config.dateRaw = datetime.now().strftime("%m_%d_%Y")
config.datePretty = datetime.now().strftime("%B %d, %Y")

checkUpdates(config)


class TestEmail(unittest.TestCase):
    config.currentEmail = "john@gmail.com"

    def test_verify_email(self):

        result = verifyEmail(config.currentEmail, config)
        self.assertTrue(result)


class TestEmailPreCheck(unittest.IsolatedAsyncioTestCase):
    @patch("src.modules.core.email.do_async_request", new_callable=AsyncMock)
    @patch("src.modules.core.email.perform_pre_check", return_value=None)
    async def test_failed_pre_check_stops_site_request(
        self, mock_pre_check, mock_request
    ):
        site = {
            "name": "Example",
            "cat": "social",
            "pre_check": {"type": "cookie"},
        }

        result = await checkSite(
            site=site,
            method="GET",
            url="https://example.com",
            session=Mock(),
            semaphore=asyncio.Semaphore(1),
            config=Mock(),
            headers={"Cookie": "session={session_value}"},
        )

        self.assertEqual(result["status"], "ERROR")
        mock_pre_check.assert_called_once()
        mock_request.assert_not_awaited()


class TestUsername(unittest.TestCase):
    config.currentUser = "p1ngul1n0"

    def test_verify_username(self):
        result = verifyUsername(config.currentUser, config)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
