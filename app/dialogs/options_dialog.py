import os
import glob
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton,
    QSpinBox, QTabWidget, QComboBox, QButtonGroup, QRadioButton, QWidget, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QMovie,QIcon
from app.utils.db import get_saved_setting, update_setting
from app.utils.helpers import get_absolute_path, get_resource_path

class OptionsDialog(QDialog):
    def __init__(self, app=None):
        super().__init__()
        self.setWindowTitle(self.tr("Options"))
        self.setWindowIcon(QIcon(get_absolute_path('icon.png')))
        self.setFixedSize(400, 300)
        self.app = app

        # Tab widget
        tabs = QTabWidget(self)

        # General tab
        general_tab = QWidget()
        general_layout = QGridLayout()

        # Duration Time
        duration_label = QLabel(self.tr("Delay Time (seconds):"))
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 10000)  # Positive number input
        self.duration_input.setValue(get_saved_setting("duration") or 10)  # Default value 10
        general_layout.addWidget(duration_label, 0, 0)
        general_layout.addWidget(self.duration_input, 0, 1)

        # Language
        lang_label = QLabel(self.tr("Select Language:"))
        self.language_dropdown = QComboBox()
        self.language_dropdown.addItems(["English", "Македонски"])
        self.language_dropdown.setCurrentText(self.app.current_language)
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
        full_layout = QVBoxLayout()
        characters_dir = get_absolute_path('characters')  # Get absolute path for exe
        files = glob.glob(os.path.join(characters_dir, '*.gif'))  # Get all GIF files
    
        # Add option for no image to be displayed
        radio_button = QRadioButton("No media")
        radio_button.setChecked(get_saved_setting("character") == 0)
        self.character_group.addButton(radio_button, 0)
        no_img_layout = QHBoxLayout()
        no_img_layout.addWidget(radio_button)
        full_layout.addLayout(no_img_layout)

        # Layout for the characters
        characters_layout = QHBoxLayout()

        for i, file in enumerate(files, start=1):
            # Check if the file exists
            if not os.path.isfile(file):
                continue

            # Create radio button with the name of the image as label
            file_name = os.path.splitext(os.path.basename(file))[0]
            radio_button = QRadioButton(file_name.capitalize())
            radio_button.setChecked(get_saved_setting("character") == i)
            self.character_group.addButton(radio_button, i)

            # Create QLabel for displaying GIF
            gif_label = QLabel()
            gif_label.setAlignment(Qt.AlignCenter)

            # Create QMovie and load GIF file
            gif_movie = QMovie()
            gif_movie.setFileName(file)  # Use setFileName for better file path handling
            gif_movie.start()

            if not gif_movie.isValid():
                continue

            # Set static size for each GIF (90x65)
            fixed_width = 90
            fixed_height = 65
            gif_movie.setScaledSize(QSize(fixed_width, fixed_height))  # Set GIF size to 90x65

            # Set movie on the QLabel
            gif_label.setMovie(gif_movie)
            gif_movie.start()

            # Handle click event to select radio button
            gif_label.mousePressEvent = lambda _, b=radio_button: b.setChecked(True)

            # Add layout for character option
            char_layout = QVBoxLayout()
            char_layout.addWidget(gif_label)
            char_layout.addWidget(radio_button)
            characters_layout.addLayout(char_layout)
        
        full_layout.addLayout(characters_layout)
        layout.addLayout(full_layout)

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
            color_label.setFixedSize(16, 16)
            color_label.setStyleSheet(f"background-color: {color.lower()}; border: 1px solid black;")
            color_label.setAlignment(Qt.AlignCenter)
            color_label.mousePressEvent = lambda _, b=radio_button: b.setChecked(True)

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

        if language != self.app.current_language:
            self.app.change_language(language)

        update_setting("language", language)
        update_setting("duration", duration)
        update_setting("character", character)
        update_setting("background", background_file)

        if password:
            update_setting("password", password)

        QMessageBox.information(self, self.tr("Saved"), self.tr("Options saved successfully!"))
        self.accept()