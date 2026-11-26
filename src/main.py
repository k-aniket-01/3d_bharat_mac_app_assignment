
import sys

from PySide6.QtWidgets import QApplication
from src.gui import MacAddressApp


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("3D Bharat MAC Address Fetcher")
    app.setOrganizationName(
        "Micro Integrated Semiconductor Systems Pvt. Ltd."
    )

    window = MacAddressApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
