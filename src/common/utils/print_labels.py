from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PySide6.QtWidgets import QFileDialog, QMessageBox
from ..models import products

def print_labels():
    selected = []  # For simplicity, print all products, or modify to select
    if not products:
        QMessageBox.warning(None, "Erreur", "Aucun produit à imprimer")
        return

    file, _ = QFileDialog.getSaveFileName(None, "Enregistrer PDF", "", "PDF (*.pdf)")
    if not file:
        return

    c = canvas.Canvas(file, pagesize=letter)
    width, height = letter

    x = 0.5 * inch
    y = height - 0.5 * inch
    label_width = 2.5 * inch
    label_height = 1 * inch

    for product in products:
        # Draw label
        c.rect(x, y - label_height, label_width, label_height)
        c.drawString(x + 0.1 * inch, y - 0.3 * inch, f"Ref: {product.reference}")
        c.drawString(x + 0.1 * inch, y - 0.6 * inch, f"Nom: {product.name}")
        c.drawString(x + 0.1 * inch, y - 0.9 * inch, f"Prix: {product.price:.2f} €")

        x += label_width + 0.2 * inch
        if x + label_width > width:
            x = 0.5 * inch
            y -= label_height + 0.2 * inch
            if y < 0.5 * inch:
                c.showPage()
                y = height - 0.5 * inch

    c.save()
    QMessageBox.information(None, "Succès", "Étiquettes imprimées")