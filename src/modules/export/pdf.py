from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import config
import os

# Save results to PDF file
regularFontFile = os.path.join(os.getcwd(), config.ASSETS_DIRECTORY, config.FONTS_DIRECTORY, config.FONT_REGULAR_FILE)
boldFontFile = os.path.join(os.getcwd(), config.ASSETS_DIRECTORY, config.FONTS_DIRECTORY, config.FONT_BOLD_FILE)


def saveToPdf(username, prettyDate, date, results):
    pdfmetrics.registerFont(TTFont(config.FONT_NAME_REGULAR, regularFontFile))
    pdfmetrics.registerFont(TTFont(config.FONT_NAME_BOLD, boldFontFile))

    fileName = username + "_" + date + "_blackbird.pdf"
    path = os.path.join(config.saveDirectory, fileName)
    width, height = letter
    canva = canvas.Canvas(path, pagesize=letter)
    accountsCount = len(results)

    canva.drawImage(os.path.join(os.getcwd(), config.ASSETS_DIRECTORY, config.IMAGES_DIRECTORY, "blackbird-logo.png"), 35, height - 90, width=60, height=60)
    canva.setFont(config.FONT_NAME_BOLD, 15)
    canva.drawCentredString((width / 2) - 5, height - 70, "Report")
    canva.setFont(config.FONT_NAME_REGULAR, 7)
    canva.drawString(width - 90, height - 70, prettyDate)
    canva.setFont(config.FONT_NAME_REGULAR, 5)
    canva.drawString(width - 185, height - 25, "This report was generated using the Blackbird OSINT Tool.")
    
    canva.setFillColor("#EDEBED");
    canva.setStrokeColor("#BAB8BA");
    canva.rect(40, height - 160, 530, 35, stroke=1, fill=1);
    canva.setFillColor("#000000");
    usernameWidth = stringWidth(username, config.FONT_NAME_BOLD, 11)
    canva.drawImage(os.path.join(os.getcwd(), config.ASSETS_DIRECTORY, config.IMAGES_DIRECTORY, "correct.png"), (width / 2) - ((usernameWidth / 2) + 15)  , height - 147, width=10, height=10, mask='auto')
    canva.setFont(config.FONT_NAME_BOLD, 11)
    canva.drawCentredString(width / 2, height - 145, username)    

    canva.setFillColor("#FFF8C5");
    canva.setStrokeColor("#D9C884");
    canva.rect(40, height - 210, 530, 35, stroke=1, fill=1);
    canva.setFillColor("#57523f")
    canva.setFont(config.FONT_NAME_REGULAR, 8)
    canva.drawImage(os.path.join(os.getcwd(), config.ASSETS_DIRECTORY, config.IMAGES_DIRECTORY, "warning.png"), 55, height - 197, width=10, height=10, mask='auto')
    canva.drawString(70, height - 195, "Blackbird can make mistakes. Consider checking the information.")

    if (accountsCount >= 1):
        canva.setFillColor("#000000");
        canva.setFont(config.FONT_NAME_REGULAR, 15)
        canva.drawImage(os.path.join(os.getcwd(), config.ASSETS_DIRECTORY, config.IMAGES_DIRECTORY, "arrow.png"), 40, height - 240, width=12, height=12, mask='auto')
        canva.drawString(55, height - 240, f"Results ({accountsCount})")
        
        y_position = height - 270
        for result in results:
            if y_position < 72:
                canva.showPage()
                y_position = height - 130
            canva.setFont(config.FONT_NAME_REGULAR, 12)
            canva.drawString(72, y_position, f"• {result['name']}")
            siteWidth = stringWidth(f"• {result['name']}", config.FONT_NAME_REGULAR, 12)
            canva.drawImage(os.path.join(os.getcwd(), config.ASSETS_DIRECTORY, config.IMAGES_DIRECTORY, "link.png"), 77 + siteWidth, y_position, width=10, height=10, mask='auto')
            canva.linkURL(result['url'], (77 + siteWidth, y_position, 77 + siteWidth + 10, y_position + 10), relative=1)
            y_position -= 25 

    canva.save()
    config.console.print(f"💾  Saved results to '[cyan1]{fileName}[/cyan1]'")
