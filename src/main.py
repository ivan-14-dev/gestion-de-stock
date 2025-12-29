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
        background-color: #F9FAFB;
        color: #111827;
        font-family: 'Inter', 'Roboto', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 14px;
    }

    QMainWindow {
        background-color: #F9FAFB;
    }

    QPushButton {
        background-color: #2563EB;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #1D4ED8;
    }

    QPushButton:pressed {
        background-color: #1E40AF;
    }

    QLabel {
        color: #111827;
        font-size: 14px;
    }

    QLabel[data-type="title"] {
        font-weight: 600;
        font-size: 18px;
        color: #1F2937;
    }

    QLabel[data-type="subtitle"] {
        font-weight: 500;
        font-size: 16px;
        color: #374151;
    }

    QLabel[data-type="secondary"] {
        color: #6B7280;
    }

    QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 10px 12px;
        background-color: white;
        color: #111827;
        font-size: 14px;
    }

    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #2563EB;
        outline: none;
    }

    QTableWidget {
        gridline-color: #E5E7EB;
        background-color: white;
        alternate-background-color: #F9FAFB;
        selection-background-color: #DBEAFE;
        selection-color: #1E40AF;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }

    QTableWidget::item {
        padding: 8px;
        border-bottom: 1px solid #F3F4F6;
    }

    QHeaderView::section {
        background-color: #F3F4F6;
        color: #374151;
        padding: 12px 8px;
        border: none;
        border-bottom: 1px solid #E5E7EB;
        font-weight: 600;
        font-size: 13px;
    }

    QGroupBox {
        font-weight: 600;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        margin-top: 1ex;
        background-color: white;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 12px 0 12px;
        color: #2563EB;
        font-size: 16px;
        font-weight: 600;
    }

    QTabWidget::pane {
        border: 1px solid #E5E7EB;
        background-color: white;
        border-radius: 8px;
    }

    QTabBar::tab {
        background-color: #F3F4F6;
        color: #6B7280;
        padding: 12px 16px;
        border: none;
        border-bottom: 2px solid transparent;
        font-weight: 500;
        font-size: 14px;
        margin-right: 4px;
        border-radius: 8px 8px 0 0;
    }

    QTabBar::tab:selected {
        background-color: white;
        color: #2563EB;
        border-bottom: 2px solid #2563EB;
        font-weight: 600;
    }

    QTabBar::tab:hover {
        background-color: #F9FAFB;
        color: #374151;
    }

    QToolBar {
        background-color: #F3F4F6;
        border-bottom: 1px solid #E5E7EB;
        padding: 8px;
        spacing: 8px;
    }

    QToolBar QPushButton {
        background-color: #2563EB;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
        margin: 2px;
    }

    QToolBar QPushButton:hover {
        background-color: #1D4ED8;
    }

    QToolBar QPushButton:pressed {
        background-color: #1E40AF;
    }

    /* Status colors */
    QPushButton[data-status="success"] {
        background-color: #22C55E;
    }

    QPushButton[data-status="success"]:hover {
        background-color: #16A34A;
    }

    QPushButton[data-status="warning"] {
        background-color: #F59E0B;
    }

    QPushButton[data-status="warning"]:hover {
        background-color: #D97706;
    }

    QPushButton[data-status="danger"] {
        background-color: #EF4444;
    }

    QPushButton[data-status="danger"]:hover {
        background-color: #DC2626;
    }

    /* Sidebar specific */
    QWidget#sidebar {
        background-color: #F9FAFB;
        border-right: 1px solid #E5E7EB;
    }

    QWidget#sidebar QPushButton {
        background-color: transparent;
        color: #6B7280;
        text-align: left;
        padding: 12px 20px;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        font-size: 14px;
        margin: 4px 8px;
    }

    QWidget#sidebar QPushButton:hover {
        background-color: #DBEAFE;
        color: #2563EB;
    }

    QWidget#sidebar QPushButton:pressed {
        background-color: #BFDBFE;
        color: #1D4ED8;
    }

    /* Card-like styling for widgets */
    QWidget[data-role="card"] {
        background-color: white;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
    }

    /* Scroll bars */
    QScrollBar:vertical {
        background-color: #F3F4F6;
        width: 12px;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical {
        background-color: #D1D5DB;
        border-radius: 6px;
        min-height: 30px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #9CA3AF;
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