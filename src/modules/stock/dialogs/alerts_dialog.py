from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from ....common.models import products, categories, suppliers
from .settings_dialog import SETTINGS_FILE
import json
import os

class AlertsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Alertes Stock Faible")
        self.setModal(True)
        layout = QVBoxLayout(self)

        # Load threshold
        threshold = 10
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                threshold = settings.get('low_stock_threshold', 10)

        # Find low stock products
        low_stock_products = []
        for p in products:
            total_qty = sum(v.quantity for v in p.variants)
            if total_qty <= threshold:
                low_stock_products.append((p, total_qty))

        if not low_stock_products:
            layout.addWidget(QLabel("Aucun produit en stock faible"))
        else:
            label = QLabel(f"Produits avec stock ≤ {threshold}:")
            layout.addWidget(label)

            self.table = QTableWidget()
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["Référence", "Nom", "Quantité", "Catégorie"])
            self.table.setRowCount(len(low_stock_products))
            for i, (p, qty) in enumerate(low_stock_products):
                self.table.setItem(i, 0, QTableWidgetItem(p.reference))
                self.table.setItem(i, 1, QTableWidgetItem(p.name))
                self.table.setItem(i, 2, QTableWidgetItem(str(qty)))
                cat_name = next((c.name for c in categories if c.id == p.category_id), "")
                self.table.setItem(i, 3, QTableWidgetItem(cat_name))
            layout.addWidget(self.table)

        # Close button
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)