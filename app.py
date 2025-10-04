from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Lista de itens de exemplo (poderia vir de BD ou Excel)
ITEMS = [
    {"name": "Water Damage Restoration", "price": 1200},
    {"name": "Mold Removal", "price": 1500},
    {"name": "Fire Damage Repair", "price": 2500},
    {"name": "General Cleaning", "price": 500},
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected = request.form.getlist("items")
        selected_items = [item for item in ITEMS if item["name"] in selected]
        total = sum(item["price"] for item in selected_items)

        # Geração do PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, 750, "Estimate - Spero Restoration")
        p.setFont("Helvetica", 12)
        y = 700
        for item in selected_items:
            p.drawString(50, y, f"{item['name']} - ${item['price']}")
            y -= 25
        p.drawString(50, y-20, f"TOTAL: ${total}")
        p.showPage()
        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="estimate.pdf", mimetype="application/pdf")

    return render_template("index.html", items=ITEMS)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
