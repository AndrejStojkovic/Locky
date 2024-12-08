from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("About"))
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        # Add image at the center top
        image_label = QLabel()
        pixmap = QPixmap("icon.png")  # Load the image
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Scale it to fit
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
        github_label.setOpenExternalLinks(True)  # Enable link clicking
        layout.addWidget(github_label)

        # Add close button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)  # Add stretch to push the button to the right
        close_button = QPushButton(self.tr("Close"))
        close_button.setFixedWidth(100)  # Optional: Set a fixed width for the button
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        # Set layout for the dialog
        self.setLayout(layout)