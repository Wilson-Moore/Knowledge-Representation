from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath

class ImageRadius:
    @staticmethod
    def rounded_pixmap(pixmap, radius=20):
        size = pixmap.size()
        rounded = QPixmap(size)
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, size.width(), size.height()), radius, radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return rounded
