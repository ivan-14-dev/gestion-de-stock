from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QToolBar, QLineEdit, QLabel, QComboBox, QTabWidget, QFileDialog, QMessageBox, QInputDialog
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from ...common.models import products, categories, suppliers, Category, Supplier
from ...common.storage import load_data, save_data, export_csv, import_csv
from .dialogs.add_product_dialog import AddProductDialog
from .dashboard_widget import DashboardWidget
from .dialogs.barcode_dialog import BarcodeDialog
from .dialogs.stock_adjustment_dialog import StockAdjustmentDialog
from .dialogs.product_details_dialog import ProductDetailsDialog
from .dialogs.settings_dialog import SettingsDialog
from .dialogs.categories_dialog import CategoriesDialog
from .dialogs.suppliers_dialog import SuppliersDialog
from .dialogs.alerts_dialog import AlertsDialog
from ...common.utils.print_labels import print_labels
import json

class StockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Toolbar
        self.toolbar = QToolBar()
        self.layout.addWidget(self.toolbar)

        self.add_action = QAction("Ajouter Produit", self)
        self.toolbar.addAction(self.add_action)

        self.edit_action = QAction("Modifier", self)
        self.toolbar.addAction(self.edit_action)

        self.delete_action = QAction("Supprimer", self)
        self.toolbar.addAction(self.delete_action)

        self.adjust_action = QAction("Ajuster Stock", self)
        self.toolbar.addAction(self.adjust_action)

        self.details_action = QAction("Voir Détails", self)
        self.toolbar.addAction(self.details_action)

        self.barcode_action = QAction("Générer Code-Barres", self)
        self.toolbar.addAction(self.barcode_action)

        self.settings_action = QAction("Réglages Module", self)
        self.toolbar.addAction(self.settings_action)

        self.add_category_action = QAction("Ajouter Catégorie", self)
        self.toolbar.addAction(self.add_category_action)

        self.add_supplier_action = QAction("Ajouter Fournisseur", self)
        self.toolbar.addAction(self.add_supplier_action)

        self.categories_action = QAction("Gérer Catégories", self)
        self.toolbar.addAction(self.categories_action)

        self.suppliers_action = QAction("Gérer Fournisseurs", self)
        self.toolbar.addAction(self.suppliers_action)

        self.alerts_action = QAction("Alertes Stock", self)
        self.toolbar.addAction(self.alerts_action)

        self.print_action = QAction("Imprimer Étiquettes", self)
        self.toolbar.addAction(self.print_action)

        self.import_csv_action = QAction("Importer CSV", self)
        self.toolbar.addAction(self.import_csv_action)

        self.export_json_action = QAction("Exporter JSON", self)
        self.toolbar.addAction(self.export_json_action)

        self.export_csv_action = QAction("Exporter CSV", self)
        self.toolbar.addAction(self.export_csv_action)

        self.refresh_action = QAction("Rafraîchir", self)
        self.toolbar.addAction(self.refresh_action)

        # Tabs
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Table tab
        self.table_tab = QWidget()
        table_layout = QVBoxLayout(self.table_tab)

        # Search and filters
        self.search_layout = QHBoxLayout()
        table_layout.addLayout(self.search_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher...")
        self.search_layout.addWidget(self.search_input)

        self.category_filter = QComboBox()
        self.category_filter.addItem("Toutes catégories")
        self.search_layout.addWidget(self.category_filter)

        self.supplier_filter = QComboBox()
        self.supplier_filter.addItem("Tous fournisseurs")
        self.search_layout.addWidget(self.supplier_filter)

        # Table
        self.table = QTableWidget()
        table_layout.addWidget(self.table)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Référence", "Nom", "Catégorie", "Fournisseur", "Prix", "Quantité Totale", "Variants", "Actions"])

        self.tabs.addTab(self.table_tab, "Table")

        # Dashboard tab
        self.dashboard_tab = DashboardWidget()
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        # Load data
        load_data()
        self.refresh_table()

        # Connect signals
        self.add_action.triggered.connect(self.add_product)
        self.edit_action.triggered.connect(self.edit_product)
        self.delete_action.triggered.connect(self.delete_product)
        self.adjust_action.triggered.connect(self.adjust_stock)
        self.details_action.triggered.connect(self.view_details)
        self.barcode_action.triggered.connect(self.generate_barcode)
        self.settings_action.triggered.connect(self.open_settings)
        self.add_category_action.triggered.connect(self.add_category)
        self.add_supplier_action.triggered.connect(self.add_supplier)
        self.categories_action.triggered.connect(self.manage_categories)
        self.suppliers_action.triggered.connect(self.manage_suppliers)
        self.alerts_action.triggered.connect(self.show_alerts)
        self.print_action.triggered.connect(self.print_labels)
        self.import_csv_action.triggered.connect(self.import_csv)
        self.export_json_action.triggered.connect(self.export_json)
        self.export_csv_action.triggered.connect(self.export_csv)
        self.refresh_action.triggered.connect(self.refresh_table)
        self.search_input.textChanged.connect(self.filter_table)
        self.category_filter.currentIndexChanged.connect(self.filter_table)
        self.supplier_filter.currentIndexChanged.connect(self.filter_table)

    def refresh_table(self):
        self.table.setRowCount(0)
        for product in products:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(product.reference))
            self.table.setItem(row, 1, QTableWidgetItem(product.name))
            cat_name = next((c.name for c in categories if c.id == product.category_id), "")
            self.table.setItem(row, 2, QTableWidgetItem(cat_name))
            sup_name = next((s.name for s in suppliers if s.id == product.supplier_id), "")
            self.table.setItem(row, 3, QTableWidgetItem(sup_name))
            self.table.setItem(row, 4, QTableWidgetItem(f"{product.price:.2f} €"))
            total_qty = sum(v.quantity for v in product.variants)
            self.table.setItem(row, 5, QTableWidgetItem(str(total_qty)))
            variants_str = ", ".join(f"{v.size}/{v.color}: {v.quantity}" for v in product.variants)
            self.table.setItem(row, 6, QTableWidgetItem(variants_str))
            # Actions buttons would be added here

        # Update filters
        self.category_filter.clear()
        self.category_filter.addItem("Toutes catégories")
        for cat in categories:
            self.category_filter.addItem(cat.name)

        self.supplier_filter.clear()
        self.supplier_filter.addItem("Tous fournisseurs")
        for sup in suppliers:
            self.supplier_filter.addItem(sup.name)

        # Update dashboard
        self.dashboard_tab.update_dashboard()

    def filter_table(self):
        search_text = self.search_input.text().lower()
        cat_filter = self.category_filter.currentText()
        sup_filter = self.supplier_filter.currentText()

        for row in range(self.table.rowCount()):
            show = True
            if search_text:
                name = self.table.item(row, 1).text().lower()
                ref = self.table.item(row, 0).text().lower()
                if search_text not in name and search_text not in ref:
                    show = False
            if cat_filter != "Toutes catégories" and self.table.item(row, 2).text() != cat_filter:
                show = False
            if sup_filter != "Tous fournisseurs" and self.table.item(row, 3).text() != sup_filter:
                show = False
            self.table.setRowHidden(row, not show)

    def add_product(self):
        dialog = AddProductDialog(self)
        if dialog.exec():
            self.refresh_table()

    def edit_product(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un produit")
            return
        row = selected[0].row()
        ref = self.table.item(row, 0).text()
        product = next((p for p in products if p.reference == ref), None)
        if product:
            dialog = AddProductDialog(self, product)
            if dialog.exec():
                self.refresh_table()

    def delete_product(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un produit")
            return
        row = selected[0].row()
        ref = self.table.item(row, 0).text()
        product = next((p for p in products if p.reference == ref), None)
        if product:
            reply = QMessageBox.question(self, "Confirmer", f"Supprimer {product.name}?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                products.remove(product)
                save_data()
                self.refresh_table()

    def adjust_stock(self):
        dialog = StockAdjustmentDialog(self)
        if dialog.exec():
            self.refresh_table()

    def view_details(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un produit")
            return
        row = selected[0].row()
        ref = self.table.item(row, 0).text()
        product = next((p for p in products if p.reference == ref), None)
        if product:
            dialog = ProductDetailsDialog(product, self)
            dialog.exec()

    def generate_barcode(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un produit")
            return
        row = selected[0].row()
        ref = self.table.item(row, 0).text()
        dialog = BarcodeDialog(ref, self)
        dialog.exec()

    def import_csv(self):
        file, _ = QFileDialog.getOpenFileName(self, "Importer CSV", "", "CSV (*.csv)")
        if file:
            try:
                import_csv(file, 'products')
                load_data()
                self.refresh_table()
                QMessageBox.information(self, "Succès", "Import réussi")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de l'import: {str(e)}")

    def export_json(self):
        file, _ = QFileDialog.getSaveFileName(self, "Exporter JSON", "", "JSON (*.json)")
        if file:
            try:
                with open(file, 'w') as f:
                    data = []
                    for p in products:
                        d = p.__dict__.copy()
                        d['created_at'] = d['created_at'].isoformat()
                        d['updated_at'] = d['updated_at'].isoformat()
                        d['variants'] = [v.__dict__ for v in d['variants']]
                        data.append(d)
                    json.dump(data, f, indent=4)
                QMessageBox.information(self, "Succès", "Export réussi")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de l'export: {str(e)}")

    def export_csv(self):
        file, _ = QFileDialog.getSaveFileName(self, "Exporter CSV", "", "CSV (*.csv)")
        if file:
            try:
                export_csv(file, 'products')
                QMessageBox.information(self, "Succès", "Export réussi")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Erreur lors de l'export: {str(e)}")

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def add_category(self):
        name, ok = QInputDialog.getText(self, "Ajouter Catégorie", "Nom de la catégorie:")
        if ok and name.strip():
            cat_id = max((c.id for c in categories), default=0) + 1
            categories.append(Category(id=cat_id, name=name.strip()))
            save_data()
            self.refresh_table()

    def add_supplier(self):
        name, ok = QInputDialog.getText(self, "Ajouter Fournisseur", "Nom du fournisseur:")
        if ok and name.strip():
            sup_id = max((s.id for s in suppliers), default=0) + 1
            suppliers.append(Supplier(id=sup_id, name=name.strip()))
            save_data()
            self.refresh_table()

    def manage_categories(self):
        dialog = CategoriesDialog(self)
        dialog.exec()
        self.refresh_table()  # Update filters

    def manage_suppliers(self):
        dialog = SuppliersDialog(self)
        dialog.exec()
        self.refresh_table()  # Update filters

    def show_alerts(self):
        dialog = AlertsDialog(self)
        dialog.exec()

    def print_labels(self):
        print_labels()