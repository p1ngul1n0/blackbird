from pathlib import Path
from rich.markup import escape
import os


# Creates directory to save PDF, CSV and HTML content
def createSaveDirectory(config):
    folderName = generateName(config)

    strPath = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "results", Path(folderName)
    )
    config.saveDirectory = strPath
    path = Path(strPath)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        if config.verbose:
            config.console.print(
                escape(f"🆕 Created directory to save search data [{folderName}]")
            )

    if config.dump:
        if config.currentUser:
            createDumpDirectory(config.currentUser, config)

        if config.currentEmail:
            createDumpDirectory(config.currentEmail, config)

    if config.pdf:
        if config.currentUser:
            createImagesDirectory(config.currentUser, config)

        if config.currentEmail:
            createImagesDirectory(config.currentEmail, config)

    return True


def createDumpDirectory(identifier, config):
    folderName = f"dump_{identifier}"
    strPath = os.path.join(config.saveDirectory, folderName)
    path = Path(strPath)
    if not path.exists():
        if config.verbose:
            config.console.print(
                escape(f"🆕 Created directory to save dump data [{folderName}]")
            )
        path.mkdir(parents=True, exist_ok=True)


def createImagesDirectory(identifier, config):
    folderName = f"images_{identifier}"
    strPath = os.path.join(config.saveDirectory, folderName)
    path = Path(strPath)
    if not path.exists():
        if config.verbose:
            config.console.print(
                escape(f"🆕 Created directory to save images [{folderName}]")
            )
        path.mkdir(parents=True, exist_ok=True)


def generateName(config, extension=None):
    if config.currentUser:
        folderName = f"{config.currentUser}_{config.dateRaw}_blackbird"
    elif config.currentEmail:
        folderName = f"{config.currentEmail}_{config.dateRaw}_blackbird"

    if extension:
        folderName = folderName + "." + extension

    return folderName
