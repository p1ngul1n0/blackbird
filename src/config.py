import os

# WhatsMyName List
LIST_URL="https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"
LIST_DIRECTORY="data"
LIST_FILENAME="wmn-data.json"
LIST_PATH = os.path.join(os.getcwd(), LIST_DIRECTORY, LIST_FILENAME)


# Proxy
PROXY="http://127.0.0.1:8080"
USE_PROXY="FALSE"

# Logs
LOG_DIRECTORY="logs"
LOG_FILENAME="blackbird.log"
LOG_PATH = os.path.join(os.getcwd(), LOG_DIRECTORY, LOG_FILENAME)

# Assets
ASSETS_DIRECTORY="assets"
FONTS_DIRECTORY="fonts"
IMAGES_DIRECTORY="img"


# PDF
FONT_REGULAR_FILE = "MontSerrat-Regular.ttf"
FONT_BOLD_FILE = "MontSerrat-Bold.ttf"
FONT_NAME_REGULAR = "Montserrat"
FONT_NAME_BOLD = "Montserrat-Bold"