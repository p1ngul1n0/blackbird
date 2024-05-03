import os

LIST_URL="https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"
LIST_FILENAME="wmn-data.json"
PROXY="http://127.0.0.1:8080"
USE_PROXY="FALSE"
LOG_DIRECTORY="logs"
LOG_FILENAME="blackbird.log"
LOG_PATH = os.path.join(os.getcwd(), LOG_DIRECTORY, LOG_FILENAME)