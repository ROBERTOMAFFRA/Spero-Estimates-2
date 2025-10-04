from flask import Flask, render_template, request, send_file
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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
        client_name = request.form.get("client_name", "Client")
        selected = request.form.getlist("items")
        selected_items = [item for item in ITEMS if item["name"] in selected]
        total = sum(int(item["price"]) for item in selected_items)

        # Geração do PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Inserindo logo (se existir em static/logo.png)
        logo_path = os.path.join(os.path.dirname(__file__), "static", "logo.png")
        if os.path.exists(logo_path):
            p.drawImage(logo_path, 40, height - 100, width=120, height=60)

        # Cabeçalho
        p.setFont("Helvetica-Bold", 16)
        p.drawString(200, height - 50, "Spero Restoration - Estimate")

        p.setFont("Helvetica", 12)
        p.drawString(50, height - 120, f"Client: {client_name}")
        p.drawString(50, height - 140, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        # Serviços selecionados
        y = height - 180
        for item in selected_items:
            p.drawString(50, y, f"- {item['name']}  ${item['price']}")
            y -= 20

        # Total
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y - 20, f"Total: ${total}")

        p.showPage()
        p.save()

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="estimate.pdf", mimetype="application/pdf")

    return render_template("index.html", items=ITEMS)

if __name__ == "__main__":
    app.run(debug=True)
