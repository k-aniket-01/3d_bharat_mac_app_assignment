
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtNetwork import QNetworkCookie
from PySide6.QtWidgets import QMainWindow, QMessageBox
from src.config import CONFIG
from PySide6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEnginePage
)

from PySide6.QtWebEngineWidgets import QWebEngineView


WEBSITE_URL = CONFIG["website"]["url"]

COOKIE_NAME = CONFIG["cookie"]["name"].encode("utf-8")
COOKIE_DOMAIN = CONFIG["cookie"]["domain"]
COOKIE_PATH = CONFIG["cookie"]["path"]

COOKIE_SECURE = CONFIG["cookie"]["secure"]
COOKIE_HTTP_ONLY = CONFIG["cookie"]["http_only"]


class WebsiteWindow(QMainWindow):

    def __init__(self, mac_address):

        super().__init__()

        self.setWindowTitle("3D Bharat Website")
        self.resize(1200, 800)

        self.mac_address = mac_address
        self.cookie_created = False
        self.cookie_verified = False

        # 1. Create browser profile
        self.profile = QWebEngineProfile(self)

        # 2. Create browser
        self.browser = QWebEngineView(self)

        # 3. Create browser page
        self.page = QWebEnginePage(
            self.profile,
            self.browser
        )

        self.browser.setPage(self.page)
        self.setCentralWidget(self.browser)

        # 4. Connect browser signals AFTER initialization
        self.browser.loadFinished.connect(
            self.verify_cookie_visibility
        )

        # 5. Get cookie store
        self.cookie_store = self.profile.cookieStore()

        self.cookie_store.cookieAdded.connect(
            self.on_cookie_added
        )

        # 6. Set cookie before loading website
        self.create_mac_cookie()

        # 7. Timeout handling
        QTimer.singleShot(
            10000,
            self.check_cookie_timeout
        )

    def create_mac_cookie(self):

        cookie = QNetworkCookie(
            COOKIE_NAME,
            self.mac_address.encode("ascii")
        )

        cookie.setDomain(COOKIE_DOMAIN)
        cookie.setPath(COOKIE_PATH)
        cookie.setSecure(COOKIE_SECURE)
        cookie.setHttpOnly(COOKIE_HTTP_ONLY)

        origin = QUrl(WEBSITE_URL)

        self.cookie_store.setCookie(cookie, origin)

    def on_cookie_added(self, cookie):

        if cookie.name() != COOKIE_NAME:
            return

        domain = cookie.domain().lstrip(".")

        if domain != "3dbharat.com":
            return

        if self.cookie_created:
            return

        self.cookie_created = True

        self.cookie_store.cookieAdded.disconnect(
            self.on_cookie_added
        )

        self.browser.load(
            QUrl(WEBSITE_URL)
        )

    def check_cookie_timeout(self):

        if not self.cookie_created:

            QMessageBox.critical(
                self,
                "Cookie Error",
                "Unable to create the MAC address cookie."
            )

    def verify_cookie_visibility(self, success):

        print("\n========== WEBSITE DEBUG ==========")
        print("WEBSITE LOAD FINISHED:", success)
        print("CURRENT URL:", self.page.url().toString())

        if not success:
            print("Website loading failed")

            QMessageBox.warning(
                self,
                "Website Error",
                "The website could not be loaded."
            )
            return

        javascript = """
            const cookie = document.cookie
                .split(';')
                .find(item =>
                    item.trim().startsWith('mac_address=')
                );

            cookie || null;
        """

        self.page.runJavaScript(
            javascript,
            self.on_cookie_verified
        )



    def on_cookie_verified(self, cookie_value):

        print("COOKIE RECEIVED:", cookie_value)
        print("EXPECTED BSSID:", self.mac_address)

        if cookie_value is None:
            print("COOKIE TEST: FAIL - Cookie not found")
            self.cookie_verified = False
            return

        actual_value = cookie_value.split("=", 1)[1].strip()

        if actual_value == self.mac_address:
            print("COOKIE TEST: PASS")
            self.cookie_verified = True
        else:
            print("COOKIE TEST: FAIL - Value mismatch")
            self.cookie_verified = False

    def closeEvent(self, event):
        self.browser.stop()

        # Detach the page from the browser before deleting it.
        self.browser.setPage(None)

        # Delete the page before releasing its profile.
        self.page.deleteLater()

        # Keep the profile alive until the page is deleted.
        self.page.destroyed.connect(self.profile.deleteLater)

        self.mac_address = None
        super().closeEvent(event)