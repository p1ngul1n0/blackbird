import csv
import config
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', ''))

from utils.log import logError

# Save results to CSV file
def saveToCsv(username, date, results):
    try:
        fileName = username + "_" + date + "_blackbird.csv"
        path = os.path.join(config.saveDirectory, fileName)
        with open(
            path,
            "w",
            newline="",
        ) as file:
            writer = csv.writer(file)
            writer.writerow(["name", "url"])
            for result in results:
                writer.writerow([result["name"], result["url"]])
        config.console.print(f"💾  Saved results to '[cyan1]{fileName}[/cyan1]'")
    except Exception as e:
        logError(e, "Coudn't saved results to CSV file!")