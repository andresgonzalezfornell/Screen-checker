from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMenu,
    QAction,
    QSystemTrayIcon,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class App:
    """Graphical user interface class."""

    app: QApplication  # application object
    icon: QIcon  # icon
    window: QWidget  # main window
    tray: QSystemTrayIcon  # tray icon

    def __init__(self) -> None:
        self.app = QApplication([])  # Create an application instance

        # Icon
        self.icon = QIcon("media/logo.png")

        # Window
        self.window = QWidget()
        self.window.show()
        self.window.setWindowTitle("Screen checker")
        self.window.setWindowIcon(self.icon)

        # Window events
        self.window.hideEvent = lambda event: self.hide_window()  # type: ignore

        # Tray icon
        self.tray = QSystemTrayIcon(self.icon)
        self.tray.show()
        # Tray icon context menu
        menu: QMenu = QMenu()
        actions = {
            "restore": QAction("Restore", self.window),
            "quit": QAction("Quit", self.window),
        }
        actions["restore"].triggered.connect(self.show_window)
        actions["quit"].triggered.connect(self.app.quit)
        for action in actions:
            menu.addAction(actions[action])
        self.tray.setContextMenu(menu)
        # Tray icon signals
        self.tray.activated.connect(self.activate_tray)

        # Application
        self.app.exec()  # Run the application

    # Methods

    def show_window(self) -> None:
        """Show the main window."""
        self.window.show()
        self.window.setWindowState(self.window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)  # type: ignore
        self.window.activateWindow()

    def hide_window(self):
        """Hide the main window."""
        self.window.hide()
        self.window.setWindowState(self.window.windowState() | Qt.WindowMinimized)  # type: ignore

    # Slots

    def activate_tray(self, reason: QSystemTrayIcon.ActivationReason):
        """Slot when user activates tray icon.

        Args:
            reason (QSystemTrayIcon.ActivationReason): The reason for the activation.
        """
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window()
