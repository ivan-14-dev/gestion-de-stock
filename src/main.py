import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSplitter
from PySide6.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
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
            btn.clicked.connect(lambda checked, m=module: self.parent().switch_module(m))
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

    def switch_module(self, module):
        # Clear current content
        for i in reversed(range(self.content_layout.count())):
            self.content_layout.itemAt(i).widget().setParent(None)

        if module == "Gestion de Stock":
            self.content_layout.addWidget(QLabel("Module Gestion de Stock - En développement"))
        else:
            self.content_layout.addWidget(QLabel(f"Module {module} - En développement"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())