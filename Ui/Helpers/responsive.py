from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ..Helpers.Image_radius import ImageRadius

class ResponsiveMixin:
    def resizeEvent(self, event):
        # super().resizeEvent(event)
        self._resize_image()
        self.update_styles()

    def _resize_image(self):
        if hasattr(self, "image") and hasattr(self, "image_label") and not self.image.isNull():
            w = int(self.width() * 0.6)
            h = int(self.height() * 0.6)
            scaled = self.image.scaled(
                w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            radius = min(w, h) * 0.05
            self.image_label.setPixmap(ImageRadius.rounded_pixmap(scaled, radius=radius))

    def update_styles(self):
        w = self.width()
        h = self.height()

        # Navbar logo scaling
        if hasattr(self, "navbar") and hasattr(self.navbar, "logo"):
            logo_font_size = max(16, int(w * 0.03))
            self.navbar.logo.setStyleSheet(f"""
                font-size: {logo_font_size}px;
                font-weight: bold;
                color: #2c3e50;
            """)

        # Subtitle font scaling
        if hasattr(self, "subtitle"):
            subtitle_font_size = max(12, int(h * 0.03))
            self.subtitle.setStyleSheet(f"""
                font-size: {subtitle_font_size}px;
                color: #34495e;
            """)

        # Button font, width, height
        btn = None

        if hasattr(self, "start_btn"):
            btn = self.start_btn
        elif hasattr(self, "next_btn"):
            btn = self.next_btn

        if btn:
            btn_font_size = max(10, int(h * 0.01))
            btn_width = max(80, int(w * 0.2))
            btn_height = max(40, int(h * 0.1))

            btn.setFont(QFont("Arial", btn_font_size))
            btn.setFixedSize(btn_width, btn_height)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
