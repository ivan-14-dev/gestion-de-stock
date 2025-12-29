from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QToolBar, QPushButton, QLineEdit, QLabel, QComboBox, QTabWidget
from PySide6.QtCore import Qt
from .models import products, categories, suppliers
from .storage import load_data, save_data
from .add_product_dialog import AddProductDialog
from .dashboard_widget import DashboardWidget

class StockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Toolbar
        self.toolbar = QToolBar()
        self.layout.addWidget(self.toolbar)

        self.add_btn = QPushButton("Ajouter Produit")
        self.toolbar.addWidget(self.add_btn)

        self.import_csv_btn = QPushButton("Importer CSV")
        self.toolbar.addWidget(self.import_csv_btn)

        self.export_json_btn = QPushButton("Exporter JSON")
        self.toolbar.addWidget(self.export_json_btn)

        self.export_csv_btn = QPushButton("Exporter CSV")
        self.toolbar.addWidget(self.export_csv_btn)

        self.refresh_btn = QPushButton("Rafraîchir")
        self.toolbar.addWidget(self.refresh_btn)

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
        self.add_btn.clicked.connect(self.add_product)
        self.refresh_btn.clicked.connect(self.refresh_table)
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