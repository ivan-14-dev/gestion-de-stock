from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox
from .models import suppliers, Supplier
from .storage import save_data

class SuppliersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestion Fournisseurs")
        self.setModal(True)
        layout = QVBoxLayout(self)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Contact", "Email", "Téléphone"])
        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Ajouter")
        self.add_btn.clicked.connect(self.add_supplier)
        btn_layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton("Modifier")
        self.edit_btn.clicked.connect(self.edit_supplier)
        btn_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.clicked.connect(self.delete_supplier)
        btn_layout.addWidget(self.delete_btn)

        self.close_btn = QPushButton("Fermer")
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.close_btn)

        layout.addLayout(btn_layout)

        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        for sup in suppliers:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(sup.id)))
            self.table.setItem(row, 1, QTableWidgetItem(sup.name))
            self.table.setItem(row, 2, QTableWidgetItem(sup.contact))
            self.table.setItem(row, 3, QTableWidgetItem(sup.email))
            self.table.setItem(row, 4, QTableWidgetItem(sup.phone))

    def add_supplier(self):
        # Simple add dialog
        name, ok = QInputDialog.getText(self, "Ajouter Fournisseur", "Nom:")
        if ok and name.strip():
            contact, ok2 = QInputDialog.getText(self, "Contact", "Contact:")
            if ok2:
                email, ok3 = QInputDialog.getText(self, "Email", "Email:")
                if ok3:
                    phone, ok4 = QInputDialog.getText(self, "Téléphone", "Téléphone:")
                    if ok4:
                        sup_id = max((s.id for s in suppliers), default=0) + 1
                        suppliers.append(Supplier(id=sup_id, name=name.strip(), contact=contact.strip(), email=email.strip(), phone=phone.strip()))
                        save_data()
                        self.refresh_table()

    def edit_supplier(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un fournisseur")
            return
        row = selected[0].row()
        sup_id = int(self.table.item(row, 0).text())
        sup = next((s for s in suppliers if s.id == sup_id), None)
        if sup:
            name, ok = QInputDialog.getText(self, "Modifier Fournisseur", "Nom:", text=sup.name)
            if ok and name.strip():
                contact, ok2 = QInputDialog.getText(self, "Contact", "Contact:", text=sup.contact)
                if ok2:
                    email, ok3 = QInputDialog.getText(self, "Email", "Email:", text=sup.email)
                    if ok3:
                        phone, ok4 = QInputDialog.getText(self, "Téléphone", "Téléphone:", text=sup.phone)
                        if ok4:
                            sup.name = name.strip()
                            sup.contact = contact.strip()
                            sup.email = email.strip()
                            sup.phone = phone.strip()
                            save_data()
                            self.refresh_table()

    def delete_supplier(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un fournisseur")
            return
        row = selected[0].row()
        sup_id = int(self.table.item(row, 0).text())
        sup = next((s for s in suppliers if s.id == sup_id), None)
        if sup:
            reply = QMessageBox.question(self, "Confirmer", f"Supprimer {sup.name}?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                suppliers.remove(sup)
                save_data()
                self.refresh_table()

from PySide6.QtWidgets import QInputDialog