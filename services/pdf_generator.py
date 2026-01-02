from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

def generate_build_pdf(build: dict, filename: str = "pc_build.pdf") -> str:
    # Регистрация шрифта с поддержкой кириллицы
    pdfmetrics.registerFont(TTFont('DejaVu', 'fonts/DejaVuSans.ttf'))

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 50
    line_height = 20

    c.setFont("DejaVu", 16)
    c.drawString(50, y, "🖥 Чек сборки ПК")
    y -= line_height * 2

    c.setFont("DejaVu", 12)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(50, y, f"Дата сборки: {date_str}")
    y -= line_height * 2

    total_price = 0

    for key in ["cpu","motherboard","ram","gpu","cooler","psu","case"]:
        comp = build.get(key)
        if comp:
            name = comp.get("name", "—")
            price = comp.get("price", 0)
            c.drawString(50, y, f"{name}: {price} ₽")
            total_price += price
            y -= line_height

    y -= line_height
    c.setFont("DejaVu", 14)
    c.drawString(50, y, f"💰 Итоговая стоимость: {total_price} ₽")

    c.showPage()
    c.save()
    return os.path.abspath(filename)
