from database.db_connection import get_connection
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import webbrowser

# 1️⃣ Récupérer les détails et total d'une commande
def generer_facture(id_commande):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.quantite, d.prix, p.nom
        FROM details_commande d
        JOIN produits p ON d.id_produit = p.id
        WHERE d.id_commande = %s
    """, (id_commande,))
    details = cursor.fetchall()
    total = sum(d['quantite'] * float(d['prix']) for d in details)
    conn.close()
    return details, total

# 2️⃣ Générer le PDF et l'ouvrir
def generer_pdf_facture(id_commande, details, total, dossier="factures"):
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    filename = os.path.join(dossier, f"Facture_{id_commande}.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Titre
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, f"Facture #{id_commande}")

    # Date
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Ligne de séparation
    c.line(50, height - 90, width - 50, height - 90)

    # Détails
    y = height - 120
    c.setFont("Helvetica", 12)
    for d in details:
        texte = f"{d['nom']} x{d['quantite']} = {d['quantite']*d['prix']} DT"
        c.drawString(50, y, texte)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 20, f"Total: {total} DT")

    c.save()

    # Ouvre automatiquement le PDF
    webbrowser.open(filename)
    return filename
