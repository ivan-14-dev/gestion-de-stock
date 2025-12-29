import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QTimer
from .modules.stock.stock_widget import StockWidget
from .common.storage import save_data

class Sidebar(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setFixedWidth(200)
        self.setObjectName("sidebar")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        modules = [
            "Gestion de Stock",
            "Suivi des ventes quotidiennes",
            "Gestion de la clientèle",
            "Analyse des performances produits",
            "Système de promotion et remises",
            "Gestion des commandes fournisseurs",
            "Calculateur de commissions",
            "Surveillance des prix concurrents",
            "Système de réservation en magasin",
            "Tableau de bord des indicateurs clés (KPI)"
        ]

        for module in modules:
            btn = QPushButton(module)
            btn.clicked.connect(lambda checked, m=module: self.main_window.switch_module(m))
            layout.addWidget(btn)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERP Gestion de Stock")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.addWidget(QLabel("Sélectionnez un module dans la sidebar"))
        main_layout.addWidget(self.content_area)

        # Automatic backup timer (every 5 minutes)
        self.backup_timer = QTimer(self)
        self.backup_timer.timeout.connect(save_data)
        self.backup_timer.start(5 * 60 * 1000)  # 5 minutes in milliseconds

    def switch_module(self, module):
        # Clear current content
        for i in reversed(range(self.content_layout.count())):
            self.content_layout.itemAt(i).widget().setParent(None)

        if module == "Gestion de Stock":
            self.stock_widget = StockWidget()
            self.content_layout.addWidget(self.stock_widget)
        else:
            self.content_layout.addWidget(QLabel(f"Module {module} - En développement"))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Modern SaaS ERP stylesheet
    stylesheet = """
    QWidget {
        background-color: #F8F9FA;
        color: #212529;
        font-family: 'Inter', 'Roboto', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 14px;
    }

    QMainWindow {
        background-color: #F8F9FA;
    }

    QPushButton {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 500;
        font-size: 14px;
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
    }

    QPushButton:hover {
        background-color: #0056B3;
        box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
    }

    QPushButton:pressed {
        background-color: #004085;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    QLabel {
        color: #212529;
        font-size: 14px;
    }

    QLabel[data-type="title"] {
        font-weight: 600;
        font-size: 18px;
        color: #495057;
    }

    QLabel[data-type="subtitle"] {
        font-weight: 500;
        font-size: 16px;
        color: #6C757D;
    }

    QLabel[data-type="secondary"] {
        color: #6C757D;
    }

    QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
        border: 1px solid #CED4DA;
        border-radius: 4px;
        padding: 8px 12px;
        background-color: white;
        color: #495057;
        font-size: 14px;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.075);
    }

    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #007BFF;
        outline: none;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    }

    QTableWidget {
        gridline-color: #DEE2E6;
        background-color: white;
        alternate-background-color: #F8F9FA;
        selection-background-color: #D1ECF1;
        selection-color: #0C5460;
        border-radius: 4px;
        border: 1px solid #DEE2E6;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    QTableWidget::item {
        padding: 8px;
        border-bottom: 1px solid #E9ECEF;
    }

    QHeaderView::section {
        background-color: #F8F9FA;
        color: #495057;
        padding: 12px 8px;
        border: none;
        border-bottom: 2px solid #DEE2E6;
        font-weight: 600;
        font-size: 13px;
    }

    QGroupBox {
        font-weight: 600;
        border: 1px solid #DEE2E6;
        border-radius: 8px;
        margin-top: 1ex;
        background-color: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 12px 0 12px;
        color: #007BFF;
        font-size: 16px;
        font-weight: 600;
    }

    QTabWidget::pane {
        border: 1px solid #DEE2E6;
        background-color: white;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    QTabBar::tab {
        background-color: #F8F9FA;
        color: #6C757D;
        padding: 10px 16px;
        border: 1px solid #DEE2E6;
        border-bottom: none;
        font-weight: 500;
        font-size: 14px;
        margin-right: 4px;
        border-radius: 4px 4px 0 0;
    }

    QTabBar::tab:selected {
        background-color: white;
        color: #007BFF;
        border-bottom: 2px solid #007BFF;
        font-weight: 600;
    }

    QTabBar::tab:hover {
        background-color: #E9ECEF;
        color: #495057;
    }

    QToolBar {
        background-color: #F8F9FA;
        border-bottom: 1px solid #DEE2E6;
        padding: 8px;
        spacing: 4px;
    }

    QToolBar QToolButton {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
        margin: 2px;
        box-shadow: 0 1px 2px rgba(0, 123, 255, 0.2);
    }

    QToolBar QToolButton:hover {
        background-color: #0056B3;
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3);
    }

    QToolBar QToolButton:pressed {
        background-color: #004085;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
    }

    /* Status colors */
    QPushButton[data-status="success"] {
        background-color: #28A745;
        box-shadow: 0 2px 4px rgba(40, 167, 69, 0.2);
    }

    QPushButton[data-status="success"]:hover {
        background-color: #1E7E34;
        box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3);
    }

    QPushButton[data-status="warning"] {
        background-color: #FFC107;
        box-shadow: 0 2px 4px rgba(255, 193, 7, 0.2);
    }

    QPushButton[data-status="warning"]:hover {
        background-color: #E0A800;
        box-shadow: 0 4px 8px rgba(255, 193, 7, 0.3);
    }

    QPushButton[data-status="danger"] {
        background-color: #DC3545;
        box-shadow: 0 2px 4px rgba(220, 53, 69, 0.2);
    }

    QPushButton[data-status="danger"]:hover {
        background-color: #BD2130;
        box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
    }

    /* Sidebar specific */
    QWidget#sidebar {
        background-color: #F8F9FA;
        border-right: 1px solid #DEE2E6;
    }

    QWidget#sidebar QPushButton {
        background-color: transparent;
        color: #6C757D;
        text-align: left;
        padding: 12px 20px;
        border: none;
        border-radius: 4px;
        font-weight: 500;
        font-size: 14px;
        margin: 4px 8px;
    }

    QWidget#sidebar QPushButton:hover {
        background-color: #D1ECF1;
        color: #007BFF;
    }

    QWidget#sidebar QPushButton:pressed {
        background-color: #B8DAFF;
        color: #0056B3;
    }

    /* Card-like styling for widgets */
    QWidget[data-role="card"] {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #DEE2E6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Scroll bars */
    QScrollBar:vertical {
        background-color: #F8F9FA;
        width: 12px;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical {
        background-color: #ADB5BD;
        border-radius: 6px;
        min-height: 30px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #6C757D;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
    """

    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())