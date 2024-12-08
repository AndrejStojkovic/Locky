import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from app.dialogs.lock_screen import LockScreen
from app.dialogs.options_dialog import OptionsDialog
from app.dialogs.about_dialog import AboutDialog
from app.utils.db import initialize_database, get_saved_setting

class App(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_language = "English"  # Default language

    def change_language(self, language):
        self.current_language = language

def main():
    initialize_database()
    app = App(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    saved_language = get_saved_setting("language")
    if saved_language:
        app.change_language(saved_language)

    tray_icon = QSystemTrayIcon(QIcon("icon.png"))
    tray_menu = QMenu()

    tray_menu.addAction(app.tr("Run"), lambda: LockScreen().exec_())
    tray_menu.tray_menu.addSeparator()
    tray_menu.addAction(app.tr("Options..."), lambda: OptionsDialog(app).exec_())
    tray_menu.addAction(app.tr("About..."), lambda: AboutDialog().exec_())
    tray_menu.addAction(app.tr("Quit"), app.quit)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.setVisible(True)

    sys.exit(app.exec_())(False)