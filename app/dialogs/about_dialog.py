from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from app.utils.helpers import get_absolute_path

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("About"))
        self.setWindowIcon(QIcon(get_absolute_path('icon.png')))
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        # Add image at the center top
        image_label = QLabel()
        pixmap = QPixmap(get_absolute_path('icon.png'))
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        # Add text below the image
        text_label = QLabel(self.tr("Locky v1.0.0\nA funny locking screen application."))
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_label)

        # Add GitHub link
        github_label = QLabel()
        github_label.setText(
            '<a href="https://github.com/kalco/Locky" style="text-decoration:none;">Martin Rayovski</a>'
        )
        github_label.setAlignment(Qt.AlignCenter)
        github_label.setOpenExternalLinks(True)
        layout.addWidget(github_label)

        # Add close button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        close_button = QPushButton(self.tr("Close"))
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        # Set layout for the dialog
        self.setLayout(layout)