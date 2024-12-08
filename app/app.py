import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QTranslator, QSize, QTimer
from app.dialogs.lock_screen import LockScreen
from app.dialogs.options_dialog import OptionsDialog
from app.dialogs.about_dialog import AboutDialog
from app.utils.db import initialize_database, get_saved_setting
from app.utils.helpers import get_absolute_path

class App(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translator = QTranslator()
        self.current_language = "English"

    def change_language(self, language):
        """Change the application language."""
        self.current_language = language
        if language == "Македонски":
            self.translator.load("mk.qm")
        else:
            self.translator.load("")
        self.installTranslator(self.translator)

        for widget in self.allWidgets():
            if widget.isWindow():
                widget.setWindowTitle(widget.windowTitle())


class TrayApp(QSystemTrayIcon):
    def __init__(self, app):
        super().__init__()
        self.app = app

        # Load the main icon using the helper function
        self.icon_path = get_absolute_path('icon.png')
        self.icon = QIcon(self.icon_path)
        self.setIcon(self.icon)
        self.setToolTip(self.tr("Locky - Secure your screen like a boss!"))

        # Pre-create and pre-populate the tray menu (instant access)
        self.create_tray_menu()

        # Connect left-click and right-click to show the menu
        self.activated.connect(self.on_tray_icon_activated)

        # Initial state: icon is gray (disabled)
        self.lock_screen_active = False
        self.lock_screen_timer = QTimer()
        self.lock_screen_timer.setSingleShot(True)

    def create_tray_menu(self):
        """Create the tray menu and pre-populate it."""
        self.tray_menu = QMenu()
        self.run_action = self.tray_menu.addAction(self.tr("Run"), self.run_lock_screen)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.tr("Options..."), self.show_options_dialog)
        self.tray_menu.addAction(self.tr("About..."), self.show_about_dialog)
        self.tray_menu.addAction(self.tr("Quit"), self.quit_app)

        # Set the tray menu as the context menu for QSystemTrayIcon
        self.setContextMenu(self.tray_menu)
        self.preload_tray_menu()

    def preload_tray_menu(self):
        """Force the QMenu to load by showing and hiding it quickly."""
        # Force PyQt to create the menu items by showing and hiding it
        fake_cursor_position = QCursor.pos()
        self.tray_menu.popup(fake_cursor_position)
        self.tray_menu.hide()

    def run_lock_screen(self):
        """Run LockScreen after a delay specified by the duration setting."""
        if self.lock_screen_active:
            return  # Do nothing if LockScreen is already active

        # Change the icon to active immediately
        self.update_icon_state(active=True)

        # Get the duration from the database
        duration = get_saved_setting("duration")
        if not duration:
            duration = 10  # Default to 10 seconds if not set

        # Delay execution of LockScreen using QTimer
        self.lock_screen_timer.timeout.connect(self.execute_lock_screen)
        self.lock_screen_timer.start(duration * 1000)

    def execute_lock_screen(self):
        """Execute the LockScreen."""
        self.lock_screen_active = True

        # Show LockScreen
        self.lock_screen = LockScreen()
        self.lock_screen.exec_()

        # Restore default state after closing LockScreen
        self.lock_screen_active = False
        self.update_icon_state(active=False)

    def update_icon_state(self, active):
        """Update the icon to its active or inactive (gray) state."""
        if active:
            self.setIcon(self.icon)
        else:
            pixmap = self.icon.pixmap(self.icon.actualSize(QSize(32, 32)), QIcon.Disabled, QIcon.Off)
            gray_icon = QIcon(pixmap)
            self.setIcon(gray_icon)

    def show_options_dialog(self):
        """Open the Options dialog."""
        dialog = OptionsDialog(self.app)
        dialog.exec_()

    def show_about_dialog(self):
        """Open the About dialog."""
        dialog = AboutDialog()
        dialog.exec_()

    def quit_app(self):
        """Quit the application."""
        QApplication.instance().quit()

    def on_tray_icon_activated(self, reason):
        """Open the menu for both left-click and right-click events."""
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.Context):
            self.tray_menu.popup(QCursor.pos())  # Opens instantly


def main():
    initialize_database()
    app = App(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    saved_language = get_saved_setting("language")
    if saved_language:
        app.change_language(saved_language)

    # Create the TrayApp instance
    tray_icon = TrayApp(app)
    tray_icon.setVisible(True)

    sys.exit(app.exec_())