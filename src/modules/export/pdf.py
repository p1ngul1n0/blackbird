from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from modules.export.file_operations import generateName
import config
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ""))

from utils.log import logError

# Save results to PDF file
regularFontFile = os.path.join(
    os.getcwd(),
    config.ASSETS_DIRECTORY,
    config.FONTS_DIRECTORY,
    config.FONT_REGULAR_FILE,
)
boldFontFile = os.path.join(
    os.getcwd(), config.ASSETS_DIRECTORY, config.FONTS_DIRECTORY, config.FONT_BOLD_FILE
)


def saveToPdf(foundAccounts, resultType):
    try:
        pdfmetrics.registerFont(TTFont(config.FONT_NAME_REGULAR, regularFontFile))
        pdfmetrics.registerFont(TTFont(config.FONT_NAME_BOLD, boldFontFile))

        fileName = generateName("pdf")
        path = os.path.join(config.saveDirectory, fileName)

        width, height = letter
        canva = canvas.Canvas(path, pagesize=letter)
        accountsCount = len(foundAccounts)

        canva.drawImage(
            os.path.join(
                os.getcwd(),
                config.ASSETS_DIRECTORY,
                config.IMAGES_DIRECTORY,
                "blackbird-logo.png",
            ),
            35,
            height - 90,
            width=60,
            height=60,
        )
        canva.setFont(config.FONT_NAME_BOLD, 15)
        canva.drawCentredString((width / 2) - 5, height - 70, "Report")
        canva.setFont(config.FONT_NAME_REGULAR, 7)
        canva.drawString(width - 90, height - 70, config.datePretty)
        canva.setFont(config.FONT_NAME_REGULAR, 5)
        canva.drawString(
            width - 185,
            height - 25,
            "This report was generated using the Blackbird OSINT Tool.",
        )

        canva.setFillColor("#EDEBED")
        canva.setStrokeColor("#BAB8BA")
        canva.rect(40, height - 160, 530, 35, stroke=1, fill=1)
        canva.setFillColor("#000000")
        if resultType == "username":
            identifier = config.currentUser
        elif resultType == "email":
            identifier = config.currentEmail
        identifierWidth = stringWidth(identifier, config.FONT_NAME_BOLD, 11)
        canva.drawImage(
            os.path.join(
                os.getcwd(),
                config.ASSETS_DIRECTORY,
                config.IMAGES_DIRECTORY,
                "correct.png",
            ),
            (width / 2) - ((identifierWidth / 2) + 15),
            height - 147,
            width=10,
            height=10,
            mask="auto",
        )
        canva.setFont(config.FONT_NAME_BOLD, 11)
        canva.drawCentredString(width / 2, height - 145, identifier)

        canva.setFillColor("#FFF8C5")
        canva.setStrokeColor("#D9C884")
        canva.rect(40, height - 210, 530, 35, stroke=1, fill=1)
        canva.setFillColor("#57523f")
        canva.setFont(config.FONT_NAME_REGULAR, 8)
        canva.drawImage(
            os.path.join(
                os.getcwd(),
                config.ASSETS_DIRECTORY,
                config.IMAGES_DIRECTORY,
                "warning.png",
            ),
            55,
            height - 197,
            width=10,
            height=10,
            mask="auto",
        )
        canva.drawString(
            70,
            height - 195,
            "Blackbird can make mistakes. Consider checking the information.",
        )

        if accountsCount >= 1:
            canva.setFillColor("#000000")
            canva.setFont(config.FONT_NAME_REGULAR, 15)
            canva.drawImage(
                os.path.join(
                    os.getcwd(),
                    config.ASSETS_DIRECTORY,
                    config.IMAGES_DIRECTORY,
                    "arrow.png",
                ),
                40,
                height - 240,
                width=12,
                height=12,
                mask="auto",
            )
            canva.drawString(55, height - 240, f"Results ({accountsCount})")

            y_position = height - 270
            for result in foundAccounts:
                if y_position < 72:
                    canva.showPage()
                    y_position = height - 130

                canva.setFont(config.FONT_NAME_REGULAR, 12)
                canva.drawString(72, y_position, f"• {result['name']}")

                siteWidth = stringWidth(
                    f"• {result['name']}", config.FONT_NAME_REGULAR, 12
                )
                canva.drawImage(
                    os.path.join(
                        os.getcwd(),
                        config.ASSETS_DIRECTORY,
                        config.IMAGES_DIRECTORY,
                        "link.png",
                    ),
                    77 + siteWidth,
                    y_position,
                    width=10,
                    height=10,
                    mask="auto",
                )
                canva.linkURL(
                    result["url"],
                    (77 + siteWidth, y_position, 77 + siteWidth + 10, y_position + 10),
                    relative=1,
                )

                if result["metadata"]:
                    y_position -= 25
                    canva.setFont(config.FONT_NAME_REGULAR, 7)
                    for data in result["metadata"]:
                        for d in data:
                            if d["type"] == "String":
                                canva.drawString(
                                    100, y_position, f"• {d['name']}: {d['value']}"
                                )
                                y_position -= 25
                            elif d["type"] == "Array":
                                canva.drawString(100, y_position, f"• {d['name']}:")
                                y_position -= 25
                                for value in d["value"]:
                                    canva.drawString(150, y_position, f"• {value}:")
                                    y_position -= 25
                            elif d["type"] == "Image":
                                y_position -= 25
                                canva.drawImage(
                                    os.path.join(
                                        config.saveDirectory,
                                        f"images_{identifier}",
                                        f"{result['name']}_image.jpg",
                                    ),
                                    110,
                                    y_position,
                                    width=30,
                                    height=30,
                                )
                                y_position -= 25

                y_position -= 25
        canva.save()
        config.console.print(f"💾  Saved results to '[cyan1]{fileName}[/cyan1]'")
        return True
    except Exception as e:
        logError(e, "Coudn't saved results to PDF file!")
        return False
