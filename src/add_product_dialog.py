from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
from .models import products, categories, suppliers, Product, Variant
from .storage import save_data
import uuid

class AddProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        self.setWindowTitle("Modifier Produit" if product else "Ajouter Produit")
        self.setModal(True)
        layout = QVBoxLayout(self)

        # Reference
        ref_layout = QHBoxLayout()
        ref_layout.addWidget(QLabel("Référence:"))
        self.ref_input = QLineEdit()
        ref_layout.addWidget(self.ref_input)
        layout.addLayout(ref_layout)

        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nom:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Category
        cat_layout = QHBoxLayout()
        cat_layout.addWidget(QLabel("Catégorie:"))
        self.cat_combo = QComboBox()
        for cat in categories:
            self.cat_combo.addItem(cat.name, cat.id)
        cat_layout.addWidget(self.cat_combo)
        layout.addLayout(cat_layout)

        # Supplier
        sup_layout = QHBoxLayout()
        sup_layout.addWidget(QLabel("Fournisseur:"))
        self.sup_combo = QComboBox()
        for sup in suppliers:
            self.sup_combo.addItem(sup.name, sup.id)
        sup_layout.addWidget(self.sup_combo)
        layout.addLayout(sup_layout)

        # Price
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("Prix:"))
        self.price_input = QLineEdit()
        price_layout.addWidget(self.price_input)
        layout.addLayout(price_layout)

        # Variants (simple: size, color, quantity)
        var_layout = QHBoxLayout()
        var_layout.addWidget(QLabel("Taille:"))
        self.size_input = QLineEdit()
        var_layout.addWidget(self.size_input)
        var_layout.addWidget(QLabel("Couleur:"))
        self.color_input = QLineEdit()
        var_layout.addWidget(self.color_input)
        var_layout.addWidget(QLabel("Quantité:"))
        self.qty_input = QLineEdit()
        var_layout.addWidget(self.qty_input)
        layout.addLayout(var_layout)

        # Photo
        photo_layout = QHBoxLayout()
        photo_layout.addWidget(QLabel("Photo:"))
        self.photo_label = QLabel("Aucune sélectionnée")
        photo_layout.addWidget(self.photo_label)
        self.photo_btn = QPushButton("Sélectionner")
        self.photo_btn.clicked.connect(self.select_photo)
        photo_layout.addWidget(self.photo_btn)
        layout.addLayout(photo_layout)

        # Description
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Description:"))
        self.desc_input = QLineEdit()
        desc_layout.addWidget(self.desc_input)
        layout.addLayout(desc_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Modifier" if self.product else "Ajouter")
        self.ok_btn.clicked.connect(self.accept_product)
        btn_layout.addWidget(self.ok_btn)
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.photo_path = ""

        # Prefill if editing
        if self.product:
            self.ref_input.setText(self.product.reference)
            self.name_input.setText(self.product.name)
            cat_index = self.cat_combo.findData(self.product.category_id)
            if cat_index >= 0:
                self.cat_combo.setCurrentIndex(cat_index)
            sup_index = self.sup_combo.findData(self.product.supplier_id)
            if sup_index >= 0:
                self.sup_combo.setCurrentIndex(sup_index)
            self.price_input.setText(str(self.product.price))
            if self.product.variants:
                v = self.product.variants[0]
                self.size_input.setText(v.size)
                self.color_input.setText(v.color)
                self.qty_input.setText(str(v.quantity))
            self.desc_input.setText(self.product.description)
            if self.product.photos:
                self.photo_path = self.product.photos[0]
                self.photo_label.setText(self.photo_path.split('/')[-1])

    def select_photo(self):
        file, _ = QFileDialog.getOpenFileName(self, "Sélectionner Photo", "", "Images (*.png *.jpg *.jpeg)")
        if file:
            self.photo_path = file
            self.photo_label.setText(file.split('/')[-1])

    def accept_product(self):
        try:
            ref = self.ref_input.text().strip()
            name = self.name_input.text().strip()
            cat_id = self.cat_combo.currentData()
            sup_id = self.sup_combo.currentData()
            price = float(self.price_input.text())
            size = self.size_input.text().strip()
            color = self.color_input.text().strip()
            qty = int(self.qty_input.text())
            desc = self.desc_input.text().strip()

            if not ref or not name:
                QMessageBox.warning(self, "Erreur", "Référence et nom requis")
                return

            if self.product:
                # Update existing
                self.product.reference = ref
                self.product.name = name
                self.product.category_id = cat_id
                self.product.supplier_id = sup_id
                self.product.price = price
                self.product.variants = [Variant(size=size, color=color, quantity=qty, sku=f"{ref}-{size}-{color}")]
                self.product.photos = [self.photo_path] if self.photo_path else []
                self.product.description = desc
                self.product.updated_at = datetime.now()
            else:
                # Add new
                prod_id = max((p.id for p in products), default=0) + 1
                variant = Variant(size=size, color=color, quantity=qty, sku=f"{ref}-{size}-{color}")
                prod = Product(
                    id=prod_id,
                    reference=ref,
                    name=name,
                    category_id=cat_id,
                    supplier_id=sup_id,
                    price=price,
                    variants=[variant],
                    photos=[self.photo_path] if self.photo_path else [],
                    description=desc
                )
                products.append(prod)
            save_data()
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Prix et quantité doivent être numériques")