import sys
import keyboard
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication, QHBoxLayout
from PyQt5.QtGui import QMovie
from app.utils.db import get_saved_setting

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
        if background == 2:  # If background is 2, use black gradient
            self.setStyleSheet("""
                QDialog {
                    background: qradialgradient(cx: 0.5, cy: 0.5, radius: 1,
                                                fx: 0.5, fy: 0.5,
                                                stop: 0 #222, stop: 1 #000);
                }
            """)
        else:  # Default to pink gradient
            self.setStyleSheet("""
                QDialog {
                    background: qradialgradient(cx: 0.5, cy: 0.5, radius: 1,
                                                fx: 0.5, fy: 0.5,
                                                stop: 0 #FFC0CB, stop: 1 #FF69B4);
                }
            """)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        # Typewriter text above the input field
        self.typewriter_label = QLabel("")
        self.typewriter_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
            }
        """)
        self.typewriter_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.typewriter_label)

        # GIF Animation
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)
        if character == 1:  # If character is 1, use ninja1.gif
            gif_path = "ninja1.gif"
        else:  # Default to ninja2.gif
            gif_path = "ninja2.gif"
        self.gif_movie = QMovie(gif_path)  # Replace with your actual GIF paths
        self.gif_movie.setScaledSize(QtCore.QSize(483, 219))  # Adjust size if needed
        self.gif_label.setMovie(self.gif_movie)
        layout.addWidget(self.gif_label)
        self.gif_movie.start()

        # Horizontal Layout for Input and Button
        input_button_layout = QHBoxLayout()

        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #333;
                color: white;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                width: 200px; /* Set width to 200px */
            }
        """)
        self.password_input.setFixedWidth(200)  # Explicitly set the fixed width
        self.password_input.setAlignment(Qt.AlignCenter)
        input_button_layout.addWidget(self.password_input)

        # Unlock Button
        unlock_button = QPushButton("Unlock")
        unlock_button.setStyleSheet("""
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
        unlock_button.setFixedHeight(40)  # Match button height with the input field
        unlock_button.setFixedWidth(80)  # Optional: set fixed width for consistency
        unlock_button.clicked.connect(self.handle_unlock)

        # Add 5px margin to the left of the button
        input_button_layout.addSpacing(5)  # Add spacing between input and button
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
            "Welcome to the Lock Screen.",
            "You need to enter your password to continue.",
            "Security is our priority."
        ]
        self.current_phrase_index = 0
        self.current_text_index = 0
        self.typewriter_speed = 50  # Milliseconds between character updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_typewriter_text)

    def showEvent(self, event):
        """Start the typewriter effect when the dialog is shown."""
        super().showEvent(event)
        self.start_typewriter_effect()
        keyboard.block_key('esc')  # Disable Esc key
        keyboard.block_key('windows')  # Disable Windows key

    def closeEvent(self, event):
        """Re-enable blocked keys when the lock screen is closed."""
        keyboard.unblock_key('esc')
        keyboard.unblock_key('windows')

    def start_typewriter_effect(self):
        """Start the typewriter effect for the current phrase."""
        if self.current_phrase_index < len(self.typewriter_phrases):
            self.current_text_index = 0
            self.typewriter_label.setText("")  # Clear the label for the next phrase
            self.timer.start(self.typewriter_speed)
        else:
            self.timer.stop()  # Stop the timer after the last phrase

    def update_typewriter_text(self):
        """Update the label with the typewriter effect."""
        current_phrase = self.typewriter_phrases[self.current_phrase_index]
        if self.current_text_index < len(current_phrase):
            current_text = self.typewriter_label.text()
            next_character = current_phrase[self.current_text_index]
            self.typewriter_label.setText(current_text + next_character)
            self.current_text_index += 1
        else:
            # Move to the next phrase after a short pause
            self.timer.stop()
            self.current_phrase_index += 1
            QTimer.singleShot(1000, self.start_typewriter_effect)  # Pause 1 second before the next phrase

    def keyPressEvent(self, event):
        """Disable Esc key functionality."""
        if event.key() == Qt.Key_Escape:
            return  # Ignore the Esc key
        super().keyPressEvent(event)

    def handle_unlock(self):
        """Handle password unlocking."""
        password = self.password_input.text()
        correct_password = get_saved_setting("password")  # Use `get_saved_setting` for password
        if password == correct_password:
            # Unlock: Close the lock screen
            self.accept()
        else:
            # Display an error message
            self.error_label.setText("Incorrect password. Please try again.")