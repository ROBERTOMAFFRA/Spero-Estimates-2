from flask import Flask, render_template, request, send_file
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime

app = Flask(__name__)

# Lista de serviços
ITEMS = [
    {"name": "Water Damage Restoration", "price": 1200},
    {"name": "Mold Removal", "price": 1500},
    {"name": "Fire Damage Repair", "price": 2500},
    {"name": "General Cleaning", "price": 500},
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        client_name = request.form.get("client_name")
        selected = request.form.getlist("items")
        selected_items = [item for item in ITEMS if item["name"] in selected]
        total = sum(int(item["price"]) for item in selected_items)

        # (continua sua lógica de gerar PDF...)

        # Aqui você provavelmente já retorna o PDF
        # return send_file(...)

    # 👇 ESTA LINHA ESTAVA FALTANDO
    return render_template("index.html", items=ITEMS)



        

        # Geração do PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Logo (coloque um arquivo logo.png na pasta do projeto)
        logo_path = "static/logo.png"
        if os.path.exists(logo_path):
            p.drawImage(logo_path, 40, height - 80, width=100, height=50)

        # Cabeçalho
        p.setFont("Helvetica-Bold", 16)
        p.drawString(160, height - 50, "Spero Restoration - Estimate")
        p.setFont("Helvetica", 10)
        p.drawString(160, height - 65, f"Data: {datetime.today().strftime('%d/%m/%Y')}")

        # Nome do cliente
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, height - 120, f"Cliente: {client_name}")

        # Tabela de serviços
        y = height - 160
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, y, "Serviço")
        p.drawString(400, y, "Preço (USD)")
        p.line(40, y - 5, 550, y - 5)

        p.setFont("Helvetica", 12)
        y -= 25
        for item in selected_items:
            p.drawString(40, y, item['name'])
            p.drawString(400, y, f"${item['price']}")
            y -= 20

        # Total
        p.setFont("Helvetica-Bold", 12)
        p.setFillColor(colors.red)
        p.drawString(40, y - 20, f"TOTAL: ${total}")
        p.setFillColor(colors.black)

        # Rodapé
        p.setFont("Helvetica-Oblique", 10)
        p.drawString(40, 40, "Spero Restoration - contato@spero.com | (123) 456-7890")

        p.save()
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name="estimate.pdf", mimetype="application/pdf")

    return render_template("index.html", items=ITEMS)

