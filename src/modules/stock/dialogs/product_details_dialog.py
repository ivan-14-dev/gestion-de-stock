from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from PySide6.QtCore import Qt
from ....common.models import products, categories, suppliers, movements

class ProductDetailsDialog(QDialog):
    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.product = product
        self.setWindowTitle(f"Détails - {product.name}")
        self.setModal(True)
        layout = QVBoxLayout(self)

        # Product info
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f"Référence: {product.reference}"))
        info_layout.addWidget(QLabel(f"Nom: {product.name}"))
        cat_name = next((c.name for c in categories if c.id == product.category_id), "")
        info_layout.addWidget(QLabel(f"Catégorie: {cat_name}"))
        sup_name = next((s.name for s in suppliers if s.id == product.supplier_id), "")
        info_layout.addWidget(QLabel(f"Fournisseur: {sup_name}"))
        info_layout.addWidget(QLabel(f"Prix: {product.price:.2f} €"))
        info_layout.addWidget(QLabel(f"Description: {product.description}"))
        layout.addLayout(info_layout)

        # Variants table
        var_label = QLabel("Variants:")
        layout.addWidget(var_label)
        self.var_table = QTableWidget()
        self.var_table.setColumnCount(3)
        self.var_table.setHorizontalHeaderLabels(["Taille", "Couleur", "Quantité"])
        self.var_table.setRowCount(len(product.variants))
        for i, v in enumerate(product.variants):
            self.var_table.setItem(i, 0, QTableWidgetItem(v.size))
            self.var_table.setItem(i, 1, QTableWidgetItem(v.color))
            self.var_table.setItem(i, 2, QTableWidgetItem(str(v.quantity)))
        layout.addWidget(self.var_table)

        # History table
        hist_label = QLabel("Historique mouvements:")
        layout.addWidget(hist_label)
        self.hist_table = QTableWidget()
        self.hist_table.setColumnCount(4)
        self.hist_table.setHorizontalHeaderLabels(["Date", "Type", "Quantité", "Raison"])
        prod_movements = [m for m in movements if m.product_id == product.id]
        self.hist_table.setRowCount(len(prod_movements))
        for i, m in enumerate(sorted(prod_movements, key=lambda x: x.date, reverse=True)):
            self.hist_table.setItem(i, 0, QTableWidgetItem(m.date.strftime("%Y-%m-%d %H:%M")))
            self.hist_table.setItem(i, 1, QTableWidgetItem("Entrée" if m.type == "in" else "Sortie"))
            self.hist_table.setItem(i, 2, QTableWidgetItem(str(m.quantity)))
            self.hist_table.setItem(i, 3, QTableWidgetItem(m.reason))
        layout.addWidget(self.hist_table)

        # Close button
        btn_layout = QHBoxLayout()
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)