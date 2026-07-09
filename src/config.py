import os

# Project root, so paths work regardless of the current working directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# List directory
LIST_DIRECTORY = "data"

# Username List
USERNAME_LIST_URL = (
    "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"
)
USERNAME_LIST_FILENAME = "wmn-data.json"
USERNAME_LIST_PATH = os.path.join(PROJECT_ROOT, LIST_DIRECTORY, USERNAME_LIST_FILENAME)
USERNAME_METADATA_LIST_FILENAME = "wmn-metadata.json"
USERNAME_METADATA_LIST_PATH = os.path.join(
    PROJECT_ROOT, LIST_DIRECTORY, USERNAME_METADATA_LIST_FILENAME
)

# Email List
EMAIL_LIST_FILENAME = "email-data.json"
EMAIL_LIST_PATH = os.path.join(PROJECT_ROOT, LIST_DIRECTORY, EMAIL_LIST_FILENAME)

# Logs
LOG_DIRECTORY = "logs"
LOG_FILENAME = "blackbird.log"
LOG_PATH = os.path.join(PROJECT_ROOT, LOG_DIRECTORY, LOG_FILENAME)

# Splash text
SPLASH_PATH = os.path.join(PROJECT_ROOT, "assets", "text", "splash.txt")

# TLS verification is on by default; --insecure flips it off
insecure = False

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