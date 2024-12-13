import sys
import keyboard
import mouse
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QTranslator, QSize, QTimer, QEvent,QObject, QThread, pyqtSignal
from app.dialogs.lock_screen import LockScreen
from app.dialogs.options_dialog import OptionsDialog
from app.dialogs.about_dialog import AboutDialog
from app.utils.db import initialize_database, get_saved_setting
from app.utils.helpers import get_absolute_path, get_resource_path


class App(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translator = QTranslator()
        self.current_language = "English"
        self.active = False

    def change_language(self, language):
        """Change the application language."""
        self.current_language = language
        if language == "Македонски":
            qm_path = get_resource_path('app/translations/mk.qm')
            self.translator.load(qm_path)
        else:
            qm_path = get_resource_path('app/translations/en.qm')
            self.translator.load(qm_path)

        self.installTranslator(self.translator)

        # Update all window titles to reflect the language change
        for widget in self.allWidgets():
            if widget.isWindow():
                widget.setWindowTitle(widget.windowTitle())

class TrayApp(QSystemTrayIcon, QObject):
    trigger_lock_screen = pyqtSignal()  # Custom signal to trigger lock screen on the main thread

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
        self.update_active_state(active=False)

        # Inactivity timer and lock logic
        self.inactivity_timer = QTimer()
        self.inactivity_timer.setSingleShot(True)
        self.lock_screen_ready = False  # Lock screen is ready after the inactivity timer

        # Connect signal to method to ensure it runs on the main thread
        self.trigger_lock_screen.connect(self.execute_lock_screen)

    def create_tray_menu(self):
        """Create the tray menu and pre-populate it."""
        self.tray_menu = QMenu()
        self.run_action = self.tray_menu.addAction(self.tr("Enabled" if self.app.active else "Disabled"), self.set_inactivity_timer)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.tr("Options..."), self.show_options_dialog)
        self.tray_menu.addAction(self.tr("About..."), self.show_about_dialog)
        self.tray_menu.addAction(self.tr("Quit"), self.quit_app)

        # Set the tray menu as the context menu for QSystemTrayIcon
        self.setContextMenu(self.tray_menu)
        self.preload_tray_menu()

    def preload_tray_menu(self):
        """Force the QMenu to load by showing and hiding it quickly."""
        fake_cursor_position = QCursor.pos()
        self.tray_menu.popup(fake_cursor_position)
        self.tray_menu.hide()

    def update_run_action_text(self):
        self.run_action.setText("Enabled" if self.app.active else "Disabled")

    def set_inactivity_timer(self):
        """Start the countdown for inactivity."""
        if self.lock_screen_active:
            return  # Do nothing if LockScreen is already active

        # Change the active state immediately
        self.update_active_state(active=not self.app.active)

        # Get the duration from the database
        duration = get_saved_setting("duration")
        if not duration:
            duration = 5  # Default to 5 seconds if not set

        if self.app.active:
            # Start the inactivity timer
            self.lock_screen_ready = False  # Lock screen is not ready until the countdown finishes
            self.inactivity_timer.timeout.connect(self.enable_lock_screen_on_input)
            self.inactivity_timer.start(duration * 1000)  # Convert to milliseconds
        else:
            # Stop the inactivity timer
            self.lock_screen_ready = False
            self.inactivity_timer.stop()

    def enable_lock_screen_on_input(self):
        """Enable lock screen and wait for the first global user input."""
        self.lock_screen_ready = True  # Enable lock screen trigger on next input

        # Start global listeners for keyboard and mouse
        mouse.hook(self.on_user_input_detected)  # Hooks all mouse events (move, click, scroll)
        keyboard.on_press(self.on_user_input_detected)  # Hooks keyboard events

    def on_user_input_detected(self, event=None):
        """Detects first user input (keyboard or mouse) after inactivity timer finishes."""
        if self.lock_screen_ready and not self.lock_screen_active:
            self.stop_global_listeners()
            self.trigger_lock_screen.emit()  # Trigger lock screen **ON THE MAIN THREAD**

    def stop_global_listeners(self):
        """Stop the global listeners for mouse and keyboard input."""
        mouse.unhook_all()
        keyboard.unhook_all()

    def execute_lock_screen(self):
        """Execute the LockScreen on the main thread."""
        if self.lock_screen_active:
            return

        self.lock_screen_active = True
        self.lock_screen_ready = False  # Reset the flag

        self.lock_screen = LockScreen()
        self.lock_screen.exec_()

        # Restore default state after closing LockScreen
        self.lock_screen_active = False
        self.update_active_state(active=False)
        keyboard.unblock_key('esc')
        keyboard.unblock_key('win')

    def update_active_state(self, active):
        """Update the global active state of the app."""
        self.app.active = active
        self.update_run_action_text()

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
            self.tray_menu.popup(QCursor.pos())

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