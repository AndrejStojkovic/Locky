import os
import sqlite3

import keyboard
import mouse
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize,QTimer, QPropertyAnimation, QUrl, pyqtSlot, QMetaObject, QThread, QLoggingCategory, QTranslator
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QDialog, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QSpinBox, QTabWidget, QMessageBox, QWidget, QHBoxLayout, QComboBox, QGridLayout, QButtonGroup, QRadioButton
from PyQt5.QtGui import QIcon, QMovie, QPixmap


# Database setup
def get_saved_setting(key):
    conn = sqlite3.connect("app_data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT {key} FROM settings WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def update_setting(key, value):
    conn = sqlite3.connect("app_data.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE settings SET {key} = ? WHERE id = 1", (value,))
    conn.commit()
    conn.close()

class LockScreen(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Unlock Screen")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(QApplication.desktop().screenGeometry())

        # Full-screen setup
        self.setWindowState(Qt.WindowFullScreen)

        # Apply a radial gradient background using QSS
        self.setStyleSheet("""
            QDialog {
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 1,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #222, stop: 1 #000);
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
        self.gif_movie = QMovie("ninja.gif")  # Replace with your GIF file path
        self.gif_movie.setScaledSize(QtCore.QSize(483, 219))  # Adjust size if needed
        self.gif_label.setMovie(self.gif_movie)
        layout.addWidget(self.gif_label)
        self.gif_movie.start()

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
                width: 300px;
            }
        """)
        self.password_input.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.password_input)

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
        unlock_button.clicked.connect(self.handle_unlock)
        layout.addWidget(unlock_button)

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
        self.main_window.hide()  # Minimize app to tray
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
        correct_password = get_stored_password()
        if password == correct_password:
            # Unlock: Close the lock screen and return to the main window
            self.accept()
            self.main_window.show()
            self.main_window.switch.setChecked(False)
            self.main_window.locked = False
        else:
            # Display an error message
            self.error_label.setText("Incorrect password. Please try again.")

# Options Dialog
class OptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Options"))
        self.setFixedSize(400, 300)
        self.parent = parent

        # Tab widget
        tabs = QTabWidget(self)

        # General tab
        general_tab = QWidget()
        general_layout = QGridLayout()

        # Duration Time
        duration_label = QLabel(self.tr("Duration Time (seconds):"))
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 10000)  # Positive number input
        self.duration_input.setValue(get_saved_setting("duration") or 10)  # Default value 10
        general_layout.addWidget(duration_label, 0, 0)
        general_layout.addWidget(self.duration_input, 0, 1)

        # Language
        lang_label = QLabel(self.tr("Select Language:"))
        self.language_dropdown = QComboBox()
        self.language_dropdown.addItems(["English", "Македонски"])
        self.language_dropdown.setCurrentText(self.parent.app.current_language)
        general_layout.addWidget(lang_label, 1, 0)
        general_layout.addWidget(self.language_dropdown, 1, 1)

        # Change Password
        password_label = QLabel(self.tr("Change Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText(self.tr("Enter new password"))
        general_layout.addWidget(password_label, 2, 0)
        general_layout.addWidget(self.password_input, 2, 1)

        general_tab.setLayout(general_layout)
        tabs.addTab(general_tab, self.tr("General"))

        # Style tab
        style_tab = QWidget()
        style_layout = QVBoxLayout()

        # Character input
        character_label = QLabel(self.tr("Choose Character:"))
        style_layout.addWidget(character_label)

        self.character_group = QButtonGroup()
        character_layout = QHBoxLayout()
        self.load_character_options(character_layout)
        style_layout.addLayout(character_layout)

        # Background selection
        background_label = QLabel(self.tr("Choose Background Color:"))
        style_layout.addWidget(background_label)

        background_layout = QHBoxLayout()
        self.load_background_options(background_layout)
        style_layout.addLayout(background_layout)

        style_tab.setLayout(style_layout)
        tabs.addTab(style_tab, self.tr("Style"))

        # Save and Cancel buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton(self.tr("Save"))
        save_button.clicked.connect(self.save_options)
        button_layout.addWidget(save_button)
        cancel_button = QPushButton(self.tr("Cancel"))
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def load_character_options(self, layout):
        """Load and display animated characters as options."""
        characters_dir = "./characters"
        files = [f for f in os.listdir(characters_dir) if f.endswith('.gif')]

        # Get available space for displaying the GIFs
        dialog_width = self.width()  # Get dialog width
        max_width = dialog_width // 2 - 20  # Half-width of the dialog minus padding
        max_height = 150  # Set a reasonable maximum height

        for i, file in enumerate(files, start=1):
            # Create a radio button for each character
            radio_button = QRadioButton(f"{i}")
            radio_button.setChecked(get_saved_setting("character") == i)
            self.character_group.addButton(radio_button, i)

            # Create a label with the animated GIF
            image_path = os.path.join(characters_dir, file)
            gif_movie = QMovie(image_path)

            # Get original size of the GIF and calculate scale factor
            original_size = gif_movie.scaledSize()
            scale_factor = min(max_width / original_size.width(), max_height / original_size.height())
            scaled_width = int(original_size.width() * scale_factor)
            scaled_height = int(original_size.height() * scale_factor)
            gif_movie.setScaledSize(QSize(scaled_width, scaled_height))  # Scale GIF

            gif_label = QLabel()
            gif_label.setMovie(gif_movie)
            gif_movie.start()  # Start the animation

            # Handle clicking on the GIF to select the radio button
            gif_label.mousePressEvent = lambda _, b=radio_button: b.setChecked(True)

            # Add radio button and animation label
            char_layout = QVBoxLayout()
            char_layout.addWidget(gif_label)
            char_layout.addWidget(radio_button)

            # Add the character option to the layout
            layout.addLayout(char_layout)

    def load_background_options(self, layout):
        """Load and display background color options."""
        self.background_group = QButtonGroup()

        backgrounds = [
            (1, "Pink"),
            (2, "Black")
        ]

        for value, color in backgrounds:
            # Create a radio button for each background
            radio_button = QRadioButton(self.tr("Background"))
            radio_button.setChecked(get_saved_setting("background") == value)
            self.background_group.addButton(radio_button, value)

            # Create a label with a colored square
            color_label = QLabel()
            color_label.setFixedSize(30, 30)
            color_label.setStyleSheet(f"background-color: {color.lower()}; border: 1px solid black;")
            color_label.setAlignment(Qt.AlignCenter)
            color_label.mousePressEvent = lambda _, b=radio_button: b.setChecked(True)  # Select on click

            # Add the square and radio button to the layout
            bg_layout = QVBoxLayout()
            bg_layout.addWidget(color_label)
            bg_layout.addWidget(radio_button)

            layout.addLayout(bg_layout)

    def save_options(self):
        language = self.language_dropdown.currentText()
        duration = self.duration_input.value()
        password = self.password_input.text()
        character = self.character_group.checkedId()
        background_file = self.background_group.checkedId()

        if language != self.parent.app.current_language:
            self.parent.app.change_language(language)

        update_setting("language", language)
        update_setting("duration", duration)
        update_setting("character", character)
        update_setting("background", background_file)

        if password:
            update_setting("password", password)

        QMessageBox.information(self, self.tr("Saved"), self.tr("Options saved successfully!"))
        self.accept()


# About Dialog
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


# Main AppWindow
class AppWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Locky")
        self.setFixedSize(400, 300)
        self.hide()


# System Tray
class TrayApp(QSystemTrayIcon):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon("icon.png"))  # Replace with your icon path
        self.setToolTip(self.tr("Locky - Secure your screen like a boss!"))
        self.app = app

        self.tray_menu = QMenu()
        self.tray_menu.addAction(self.tr("Options"), self.show_options_dialog)
        self.tray_menu.addAction(self.tr("About"), self.show_about_dialog)
        self.tray_menu.addAction(self.tr("Quit"), self.quit_app)

        self.setContextMenu(self.tray_menu)
        self.activated.connect(self.on_tray_icon_activated)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Left click
            self.parent().show()

    def show_about_dialog(self):
        dialog = AboutDialog(self.parent())
        dialog.exec_()

    def show_options_dialog(self):
        dialog = OptionsDialog(self.parent())
        dialog.exec_()

    def quit_app(self):
        QApplication.instance().quit()


# Custom Application Class
class App(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.translator = QTranslator()
        self.current_language = "English"  # Default language

    def change_language(self, language):
        self.current_language = language
        if language == "Македонски":
            self.translator.load("mk.qm")
        else:
            self.translator.load("")
        self.installTranslator(self.translator)

        for widget in self.allWidgets():
            if widget.isWindow():
                widget.setWindowTitle(widget.windowTitle())


# Main function
def main():
    conn = sqlite3.connect("app_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        password TEXT,
        language TEXT,
        character INTEGER,
        duration INTEGER,
        background INTEGER
    )
    """)
    cursor.execute("INSERT OR IGNORE INTO settings (id, password, language, character, duration, background) VALUES (1, 'admin', 'English', 1, 10, 1)")
    conn.commit()
    conn.close()

    app = App(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    saved_language = get_saved_setting("language")
    if saved_language:
        app.change_language(saved_language)

    main_window = AppWindow(app)
    tray_icon = TrayApp(app, main_window)
    tray_icon.setVisible(True)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()