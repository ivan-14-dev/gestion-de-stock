from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import barcode
from barcode.writer import ImageWriter
import qrcode
import io

class BarcodeDialog(QDialog):
    def __init__(self, product_ref, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Code-Barres pour {product_ref}")
        layout = QVBoxLayout(self)

        # Generate barcode
        ean = barcode.get('code128', product_ref, writer=ImageWriter())
        fp = io.BytesIO()
        ean.write(fp)
        fp.seek(0)
        image = QImage()
        image.loadFromData(fp.getvalue())
        pixmap = QPixmap.fromImage(image)
        barcode_label = QLabel()
        barcode_label.setPixmap(pixmap)
        layout.addWidget(barcode_label)

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(product_ref)
        qr.make(fit=True)
        qr_image = qr.make_image(fill='black', back_color='white')
        qr_pixmap = self.pil_to_pixmap(qr_image)
        qr_label = QLabel()
        qr_label.setPixmap(qr_pixmap)
        layout.addWidget(qr_label)

        # Buttons
        btn_layout = QHBoxLayout()
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def pil_to_pixmap(self, pil_image):
        # Convert PIL to QPixmap
        pil_image = pil_image.convert('RGB')
        data = pil_image.tobytes('raw', 'RGB')
        qimage = QImage(data, pil_image.size[0], pil_image.size[1], QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)