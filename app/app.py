import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QTranslator, QSize
# from app.dialogs.lock_screen import LockScreen  # Uncomment this if LockScreen is implemented
from app.dialogs.options_dialog import OptionsDialog
from app.dialogs.about_dialog import AboutDialog
from app.utils.db import initialize_database, get_saved_setting
from app.utils.helpers import get_absolute_path

class App(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translator = QTranslator()
        self.current_language = "English"  # Default language

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

        # Load the main icon
        self.icon = QIcon(get_absolute_path('icon.png'))
        self.setIcon(self.icon)
        self.setToolTip(self.tr("Locky - Secure your screen like a boss!"))

        # Tray menu
        self.tray_menu = QMenu()
        self.run_action = self.tray_menu.addAction(self.tr("Run"), self.run_lock_screen)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.tr("Options..."), self.show_options_dialog)
        self.tray_menu.addAction(self.tr("About..."), self.show_about_dialog)
        self.tray_menu.addAction(self.tr("Quit"), self.quit_app)

        # Set the tray context menu
        self.setContextMenu(self.tray_menu)

        # Connect left-click and right-click to show the menu
        self.activated.connect(self.on_tray_icon_activated)

        # Initial state: icon is gray (disabled)
        self.lock_screen_active = False
        self.update_icon_state(active=False)  # Initial state: gray icon

    def run_lock_screen(self):
        """Run the LockScreen and toggle the icon state."""
        if self.lock_screen_active:
            # Lock screen is already active, so do nothing
            return

        self.lock_screen_active = True
        self.update_icon_state(active=True)

        # Show the LockScreen dialog
        # self.lock_screen = LockScreen()  # Uncomment this if LockScreen is implemented
        # self.lock_screen.exec_()  # Wait for LockScreen to close

        # Restore default state after closing LockScreen
        self.lock_screen_active = False
        self.update_icon_state(active=False)

    def update_icon_state(self, active):
        if active:
            self.setIcon(self.icon)
        else:
            # Use a gray version of the icon
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
            self.contextMenu().popup(QCursor.pos())


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