from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from ....common.models import products, movements, Movement
from ....common.storage import save_data
from datetime import datetime

class StockAdjustmentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajustement Stock")
        self.setModal(True)
        layout = QVBoxLayout(self)

        # Product
        prod_layout = QHBoxLayout()
        prod_layout.addWidget(QLabel("Produit:"))
        self.prod_combo = QComboBox()
        for p in products:
            self.prod_combo.addItem(f"{p.reference} - {p.name}", p.id)
        prod_layout.addWidget(self.prod_combo)
        layout.addLayout(prod_layout)

        # Type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItem("Entrée", "in")
        self.type_combo.addItem("Sortie", "out")
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)

        # Quantity
        qty_layout = QHBoxLayout()
        qty_layout.addWidget(QLabel("Quantité:"))
        self.qty_input = QLineEdit()
        qty_layout.addWidget(self.qty_input)
        layout.addLayout(qty_layout)

        # Reason
        reason_layout = QHBoxLayout()
        reason_layout.addWidget(QLabel("Raison:"))
        self.reason_input = QLineEdit()
        reason_layout.addWidget(self.reason_input)
        layout.addLayout(reason_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Ajuster")
        self.ok_btn.clicked.connect(self.adjust_stock)
        btn_layout.addWidget(self.ok_btn)
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    def adjust_stock(self):
        try:
            prod_id = self.prod_combo.currentData()
            type_ = self.type_combo.currentData()
            qty = int(self.qty_input.text())
            reason = self.reason_input.text().strip()

            product = next((p for p in products if p.id == prod_id), None)
            if not product:
                QMessageBox.warning(self, "Erreur", "Produit non trouvé")
                return

            # Update quantity
            if type_ == "in":
                product.variants[0].quantity += qty
            elif type_ == "out":
                if product.variants[0].quantity < qty:
                    QMessageBox.warning(self, "Erreur", "Quantité insuffisante")
                    return
                product.variants[0].quantity -= qty

            # Add movement
            mov_id = max((m.id for m in movements), default=0) + 1
            movement = Movement(
                id=mov_id,
                product_id=prod_id,
                type=type_,
                quantity=qty,
                reason=reason
            )
            movements.append(movement)

            save_data()
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Quantité doit être un nombre")