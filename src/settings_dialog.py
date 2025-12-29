import json
import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QComboBox, QPushButton, QMessageBox

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'settings.json')

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Réglages Module")
        self.setModal(True)
        layout = QVBoxLayout(self)

        # Low stock threshold
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Seuil stock faible:"))
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setRange(0, 1000)
        threshold_layout.addWidget(self.threshold_spin)
        layout.addLayout(threshold_layout)

        # Currency
        currency_layout = QHBoxLayout()
        currency_layout.addWidget(QLabel("Devise:"))
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["EUR", "USD", "GBP", "CAD"])
        currency_layout.addWidget(self.currency_combo)
        layout.addLayout(currency_layout)

        # Theme
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Thème:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Clair", "Sombre"])
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)

        # User role
        role_layout = QHBoxLayout()
        role_layout.addWidget(QLabel("Rôle utilisateur:"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Vendeur", "Lecture seule"])
        role_layout.addWidget(self.role_combo)
        layout.addLayout(role_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Sauvegarder")
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.load_settings()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                self.threshold_spin.setValue(settings.get('low_stock_threshold', 10))
                self.currency_combo.setCurrentText(settings.get('currency', 'EUR'))
                self.theme_combo.setCurrentText(settings.get('theme', 'Clair'))
                self.role_combo.setCurrentText(settings.get('user_role', 'Admin'))

    def save_settings(self):
        settings = {
            'low_stock_threshold': self.threshold_spin.value(),
            'currency': self.currency_combo.currentText(),
            'theme': self.theme_combo.currentText(),
            'user_role': self.role_combo.currentText()
        }
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        QMessageBox.information(self, "Succès", "Réglages sauvegardés")
        self.accept()