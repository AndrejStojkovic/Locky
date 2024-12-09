import keyboard
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication, QHBoxLayout
from app.utils.db import get_saved_setting
from app.utils.helpers import get_resource_path


class LockScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unlock Screen")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(QApplication.desktop().screenGeometry())

        # Full-screen setup
        self.setWindowState(Qt.WindowFullScreen)

        # Get character and background settings from the database
        character = get_saved_setting("character")
        background = get_saved_setting("background")

        # Apply dynamic background
        if background == 2:
            self.setStyleSheet("""
                QDialog {
                    background: qradialgradient(cx: 0.5, cy: 0.5, radius: 1,
                                                fx: 0.5, fy: 0.5,
                                                stop: 0 #222, stop: 1 #000);
                }
                QLabel {
                color: white;
                font-size: 19px;
            }
            QLineEdit {
                background-color: #333;
                color: white;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                width: 200px;
            }
             QPushButton {
                background-color: #555;
                color: white;
                border: 2px solid #777;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #777;
            }
            QPushButton:pressed {
                background-color: #999;
            }
            """)
        else:  # Default to pink gradient
            self.setStyleSheet("""
                QDialog {
                    background: qradialgradient(cx: 0.5, cy: 0.5, radius: 1,
                                                fx: 0.5, fy: 0.5,
                                                stop: 0 #FFC0CB, stop: 1 #FF69B4);
                }
                QLabel {
                color: white;
                font-size: 19px;
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.7);
                color: #333;
                border: 2px solid #ffcee2;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                width: 200px;
            }
             QPushButton {
                background-color: rgba(255, 255, 255, 0.7);
                color: #333;
                border: 2px solid #ffcee2;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f1f1f1;
            }
            QPushButton:pressed {
                background-color: #fbfbfb;
            }
            """)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        # Typewriter text
        self.typewriter_label = QLabel("")
        self.typewriter_label.setFixedWidth(500)
        self.typewriter_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.typewriter_label)

        # GIF Animation
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setFixedWidth(500)  # Independent width for animation

        # Dynamically select the character GIF
        if character == 1:
            gif_path = get_resource_path('characters/bang.gif')
        elif character == 2:
            gif_path = get_resource_path('characters/yosuke.gif')
        elif character == 3:
            gif_path = get_resource_path('characters/yu.gif')
        else:
            gif_path = get_resource_path('characters/yukiko.gif')

        self.gif_movie = QMovie(gif_path)
        self.gif_label.setMovie(self.gif_movie)
        layout.addWidget(self.gif_label)
        self.gif_movie.start()

        # Horizontal Layout for Input and Button
        input_button_layout = QHBoxLayout()

        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText(self.tr("Enter your password"))
        self.password_input.setFixedWidth(200)
        input_button_layout.addWidget(self.password_input)

        # Unlock Button
        unlock_button = QPushButton(self.tr("Unlock"))
        unlock_button.setFixedWidth(100)  # Independent width for button
        unlock_button.clicked.connect(self.handle_unlock)

        # Add 5px margin to the left of the button
        input_button_layout.addSpacing(2)
        input_button_layout.addWidget(unlock_button)

        # Add the horizontal layout to the main layout
        layout.addLayout(input_button_layout)

        # Error Label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 14px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)

        # Typewriter setup for multiple phrases
        self.typewriter_phrases = [
            self.tr("Welcome to the Lock Screen."),
            self.tr("You need to enter your password to continue."),
            self.tr("Security is our priority.")
        ]
        self.current_phrase_index = 0
        self.current_text_index = 0
        self.typewriter_speed = 50  # Milliseconds between character updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_typewriter_text)

    def showEvent(self, event):
        super().showEvent(event)
        self.start_typewriter_effect()
        keyboard.block_key('esc')
        keyboard.block_key('win')

    def closeEvent(self, event):
        keyboard.unblock_key('esc')
        keyboard.unblock_key('win')

    def start_typewriter_effect(self):
        """Start the typewriter effect for the current phrase."""
        if self.current_phrase_index < len(self.typewriter_phrases):
            self.current_text_index = 0
            self.typewriter_label.setText("")
            self.timer.start(self.typewriter_speed)
        else:
            self.timer.stop()

    def update_typewriter_text(self):
        """Update the label with the typewriter effect."""
        current_phrase = self.typewriter_phrases[self.current_phrase_index]
        if self.current_text_index < len(current_phrase):
            current_text = self.typewriter_label.text()
            next_character = current_phrase[self.current_text_index]
            self.typewriter_label.setText(current_text + next_character)
            self.current_text_index += 1
        else:
            self.timer.stop()
            self.current_phrase_index += 1
            QTimer.singleShot(1000, self.start_typewriter_effect)

    def handle_unlock(self):
        """Handle password unlocking."""
        password = self.password_input.text()
        correct_password = get_saved_setting("password")
        if password == correct_password:
            self.accept()
        else:
            self.error_label.setText(self.tr("Incorrect password. Please try again."))
