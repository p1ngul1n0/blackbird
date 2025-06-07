import sys
import os
import json

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from ..export.file_operations import generateName
from ..utils.log import logError


# Save results to JSON file
def saveToJson(results, config):
    try:
        fileName = generateName(config, "json")
        path = os.path.join(config.saveDirectory, fileName)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
        config.console.print(f"💾  Saved results to '[cyan1]{fileName}[/cyan1]'")
        return True
    except Exception as e:
        logError(e, "Couldn't save results to JSON file!", config)
        return False
