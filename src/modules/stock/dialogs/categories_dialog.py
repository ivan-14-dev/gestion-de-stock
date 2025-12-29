from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox
from ....common.models import categories, Category
from ....common.storage import save_data

class CategoriesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestion Catégories")
        self.setModal(True)
        layout = QVBoxLayout(self)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Nom"])
        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Ajouter")
        self.add_btn.clicked.connect(self.add_category)
        btn_layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton("Modifier")
        self.edit_btn.clicked.connect(self.edit_category)
        btn_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.clicked.connect(self.delete_category)
        btn_layout.addWidget(self.delete_btn)

        self.close_btn = QPushButton("Fermer")
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.close_btn)

        layout.addLayout(btn_layout)

        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        for cat in categories:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(cat.id)))
            self.table.setItem(row, 1, QTableWidgetItem(cat.name))

    def add_category(self):
        name, ok = QInputDialog.getText(self, "Ajouter Catégorie", "Nom:")
        if ok and name.strip():
            cat_id = max((c.id for c in categories), default=0) + 1
            categories.append(Category(id=cat_id, name=name.strip()))
            save_data()
            self.refresh_table()

    def edit_category(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Sélectionnez une catégorie")
            return
        row = selected[0].row()
        cat_id = int(self.table.item(row, 0).text())
        cat = next((c for c in categories if c.id == cat_id), None)
        if cat:
            name, ok = QInputDialog.getText(self, "Modifier Catégorie", "Nom:", text=cat.name)
            if ok and name.strip():
                cat.name = name.strip()
                save_data()
                self.refresh_table()

    def delete_category(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Sélectionnez une catégorie")
            return
        row = selected[0].row()
        cat_id = int(self.table.item(row, 0).text())
        cat = next((c for c in categories if c.id == cat_id), None)
        if cat:
            reply = QMessageBox.question(self, "Confirmer", f"Supprimer {cat.name}?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                categories.remove(cat)
                save_data()
                self.refresh_table()

from PySide6.QtWidgets import QInputDialog