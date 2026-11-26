
# import sys
# from PySide6.QtWidgets import QApplication, QLabel

# app = QApplication(sys.argv)

# window = QLabel("3D Bharat - Environment Setup Successful")
# window.setWindowTitle("PySide6 Test")
# window.resize(450, 120)
# window.show()

# sys.exit(app.exec())




from src.mac_address import get_connected_wifi_bssid


def main():
    try:
        bssid = get_connected_wifi_bssid()

        print("\nWi-Fi BSSID detected successfully!")
        print(f"MAC Address: {bssid}")

    except RuntimeError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
