import config
from pathlib import Path
from rich.markup import escape
import os

# Creates directory to save PDF, CSV and HTML content
def createSaveDirectory():
    if config.username and config.email:
        folderName = f"{config.username}_{config.email}_{config.dateRaw}_blackbird"
    elif config.username and not config.email:
        folderName = f"{config.username}_{config.dateRaw}_blackbird"
    elif config.email and not config.username:
        folderName = f"{config.email}_{config.dateRaw}_blackbird"

    strPath = os.path.join(os.path.dirname(__file__), '..', '..', '..', Path(folderName))
    config.saveDirectory = strPath
    path = Path(strPath)
    if not path.exists():
        if config.verbose:
            config.console.print(escape(f"🆕 Creating directory to save search data [{strPath}]"))
            path.mkdir(parents=True, exist_ok=True)

    if config.dump:
        if config.username:
            createDumpDirectory(config.username)
        
        if config.email:
            createDumpDirectory(config.email)

def createDumpDirectory(identifier):
    folderName = f"dump_{identifier}"
    strPath = os.path.join(config.saveDirectory, folderName)
    path = Path(strPath)
    if not path.exists():
        if config.verbose:
            config.console.print(escape(
                f"🆕 Creating directory to save dump data [{escape(strPath)}]")
            )
        path.mkdir(parents=True, exist_ok=True)