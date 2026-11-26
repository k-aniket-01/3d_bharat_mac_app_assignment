
import sys
from src.browser import WebsiteWindow
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox


from src.mac_address import get_connected_wifi_bssid


class MacAddressApp(QWidget):

    def __init__(self):
        super().__init__()

        self.mac_address = None
        self.browser_window = None
        self.setWindowTitle("3D Bharat - MAC Address Fetcher")
        self.setFixedSize(500, 400)

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)

        self.heading = QLabel("Fetch MAC Address")
        self.heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.heading.setStyleSheet("""
            font-size: 25px;
            font-weight: bold;
            color: #1976D2;
        """)

        self.description = QLabel(
            "Retrieve your connected Wi-Fi router MAC address"
        )
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fetch_button = QPushButton("Fetch MAC Address")
        self.fetch_button.setFixedHeight(45)
        self.fetch_button.clicked.connect(self.fetch_mac)

        self.fetch_button.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #125AA0;
            }
        """)

        self.mac_label = QLabel("MAC Address: Not fetched")
        self.mac_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mac_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            padding: 12px;
        """)

        self.launch_button = QPushButton("Launch")
        self.launch_button.setFixedHeight(45)
        self.launch_button.setEnabled(False)

        self.launch_button.clicked.connect(self.launch_website)

        self.footer = QLabel(
            "Micro Integrated Semiconductor Systems Pvt. Ltd."
        )
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.footer.setStyleSheet("""
            color: gray;
            font-size: 10px;
        """)

        layout.addWidget(self.heading)
        layout.addWidget(self.description)
        layout.addStretch()
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.mac_label)
        layout.addWidget(self.launch_button)
        layout.addStretch()
        layout.addWidget(self.footer)

        self.setLayout(layout)

    def fetch_mac(self):

        self.fetch_button.setEnabled(False)
        self.fetch_button.setText("Fetching...")

        QApplication.processEvents()

        try:

            self.mac_address = get_connected_wifi_bssid()

            self.mac_label.setText(
                f"MAC Address: {self.mac_address}"
            )

            self.launch_button.setEnabled(True)

        except RuntimeError as error:

            self.mac_address = None
            self.mac_label.setText("MAC Address: Not available")
            self.launch_button.setEnabled(False)

            QMessageBox.warning(
                self,
                "MAC Address Error",
                str(error)
            )

        finally:

            self.fetch_button.setEnabled(True)
            self.fetch_button.setText("Fetch MAC Address")

    
    def launch_website(self):
        if not self.mac_address:
            QMessageBox.warning(
                self,
                "Warning",
                "Please fetch the MAC address first."
            )
            return

        try:
            self.browser_window = WebsiteWindow( self.mac_address )
            self.browser_window.show()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Browser Error",
                f"Unable to launch website: {error}"
            )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MacAddressApp()
    window.show()

    sys.exit(app.exec())
