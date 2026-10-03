import os
import sys
from datetime import datetime

try:
    from rich.console import Console as RichConsole
except ImportError:  # pragma: no cover - Rich is optional outside the CLI runtime.
    RichConsole = None


def ensure_utf8_console():
    """Force stdout/stderr to UTF-8 for Windows terminals that default to legacy code pages."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        try:
            encoding = getattr(stream, "encoding", None)
            if encoding and "utf" in encoding.lower():
                continue
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError, ValueError):
            pass


if RichConsole is not None:
    _rich_console_init = RichConsole.__init__

    def _patched_rich_console_init(self, *args, **kwargs):
        ensure_utf8_console()
        return _rich_console_init(self, *args, **kwargs)

    RichConsole.__init__ = _patched_rich_console_init


ensure_utf8_console()

# Default runtime configuration for tests and CLI entry points.
console = RichConsole() if RichConsole is not None else None
username = None
username_file = None
permute = False
permuteall = False
csv = False
pdf = False
json = False
filter = None
no_nsfw = False
dump = False
proxy = None
verbose = False
ai = False
setup_ai = False
timeout = 30
max_concurrent_requests = 30
email = None
email_file = None
no_update = False
about = False
instagram_session_id = None
api_url = None
userAgent = None
usernameFoundAccounts = None
emailFoundAccounts = None
currentUser = None
currentEmail = None
saveDirectory = None
metadata_params = {}
username_sites = []
email_sites = []
dateRaw = datetime.now().strftime("%m_%d_%Y")
datePretty = datetime.now().strftime("%B %d, %Y")

# List directory
LIST_DIRECTORY = "data"

# Username List
USERNAME_LIST_URL = (
    "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"
)
USERNAME_LIST_FILENAME = "wmn-data.json"
USERNAME_LIST_PATH = os.path.join(os.getcwd(), LIST_DIRECTORY, USERNAME_LIST_FILENAME)
USERNAME_METADATA_LIST_FILENAME = "wmn-metadata.json"
USERNAME_METADATA_LIST_PATH = os.path.join(
    os.getcwd(), LIST_DIRECTORY, USERNAME_METADATA_LIST_FILENAME
)

# Email List
EMAIL_LIST_FILENAME = "email-data.json"
EMAIL_LIST_PATH = os.path.join(os.getcwd(), LIST_DIRECTORY, EMAIL_LIST_FILENAME)

# Logs
LOG_DIRECTORY = "logs"
LOG_FILENAME = "blackbird.log"
LOG_PATH = os.path.join(os.getcwd(), LOG_DIRECTORY, LOG_FILENAME)

# Assets
ASSETS_DIRECTORY = "assets"
FONTS_DIRECTORY = "fonts"
IMAGES_DIRECTORY = "img"


# PDF
FONT_REGULAR_FILE = "Montserrat-Regular.ttf"
FONT_BOLD_FILE = "Montserrat-Bold.ttf"
FONT_NAME_REGULAR = "Montserrat"
FONT_NAME_BOLD = "Montserrat-Bold"

aiModel = None
ai_analysis = None