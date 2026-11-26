# 3D Bharat MAC Address Fetcher

**Python Developer Technical Assignment**

**Company:** Micro Integrated Semiconductor Systems Pvt. Ltd.  
**Application:** 3D Bharat MAC Address Fetcher  
**Version:** 1.0.0  
**Website:** https://www.3dbharat.com/

---

## 1. Project Overview

The 3D Bharat MAC Address Fetcher is a Windows desktop application developed using Python and PySide6.

The application detects the BSSID (Basic Service Set Identifier) of the currently connected Wi-Fi access point, displays the detected address, and launches the 3D Bharat website in an embedded browser.

The detected BSSID is passed to the website through a JavaScript-readable browser cookie.

## 2. Features

- Detects the BSSID of the currently connected Wi-Fi network.
- Displays the detected BSSID in a desktop GUI.
- Provides a button to launch the 3D Bharat website.
- Opens the website using an embedded Qt WebEngine browser.
- Creates a cookie named `mac_address` for the `.3dbharat.com` domain.
- Allows website JavaScript to access the cookie.
- Uses a JSON configuration file for application and cookie settings.
- Includes a Windows registry configuration file.
- Supports packaging as a Windows executable using PyInstaller.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Application development |
| PySide6 | Desktop graphical interface |
| Qt WebEngine | Embedded website browser |
| Windows `netsh` | Wi-Fi interface and BSSID detection |
| JSON | Application configuration |
| PyInstaller | Windows executable packaging |

## 4. Project Structure

```text
3D_Bharat_MAC_Address_Fetcher/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── gui.py
│   ├── browser.py
│   ├── mac_address.py
│   └── config.py
│
├── config/
│   └── config.json
│
├── license/
│   └── LICENSE.txt
│
├── installer/
│   └── 3d_bharat_mac_app.reg
│
├── requirements.txt
└── README.md
```

### Source modules

| File | Responsibility |
|---|---|
| `main.py` | Application entry point |
| `gui.py` | Main PySide6 application window and user interactions |
| `mac_address.py` | Detects the connected Wi-Fi BSSID |
| `browser.py` | Creates the cookie and manages the embedded browser |
| `config.py` | Loads and validates application configuration |
| `config/config.json` | Stores website, cookie, and application settings |
| `license/LICENSE.txt` | Assignment-specific license and usage notice |
| `installer/3d_bharat_mac_app.reg` | Windows registry configuration |

## 5. Application Workflow

1. The user launches the desktop application.
2. The user clicks **Fetch MAC Address**.
3. The application executes the Windows command:

   ```powershell
   netsh wlan show interfaces
   ```

4. The application identifies the connected Wi-Fi interface and extracts its `BSSID` field.
5. The detected BSSID is displayed in the GUI.
6. The user clicks **Launch**.
7. The application creates a cookie with the following properties:

   - Name: `mac_address`
   - Domain: `.3dbharat.com`
   - Path: `/`
   - Secure: `True`
   - HttpOnly: `False`

8. The embedded browser opens:

   `https://www.3dbharat.com/`

9. JavaScript reads the cookie through `document.cookie`.
10. The application compares the cookie value with the detected BSSID and reports the verification result.

## 6. Configuration

Application settings are maintained in `config/config.json`.

Example:

```json
{
    "application": {
        "name": "3D Bharat MAC Address Fetcher",
        "version": "1.0.0",
        "company": "Micro Integrated Semiconductor Systems Pvt. Ltd."
    },
    "website": {
        "url": "https://www.3dbharat.com/"
    },
    "cookie": {
        "name": "mac_address",
        "domain": ".3dbharat.com",
        "path": "/",
        "secure": true,
        "http_only": false
    }
}
```

The configuration loader validates the required settings before the application starts.

## 7. Development Setup

### Prerequisites

- Windows 10 or Windows 11
- Python 3.12
- Internet connectivity
- Wi-Fi connection for BSSID detection

### Clone or extract the project

Open PowerShell in the project directory.

### Create a virtual environment

```powershell
python -m venv venv
```

### Activate the environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Run the application

```powershell
python -m src.main
```

## 8. BSSID Detection

The application uses the Windows `netsh` utility to retrieve wireless interface information.

Command:

```powershell
netsh wlan show interfaces
```

The application extracts the `BSSID` of the connected interface.

**Note:** BSSID and the computer's Wi-Fi adapter MAC address are different identifiers. This application retrieves the access point BSSID, not the computer's adapter MAC address.

## 9. Cookie Integration

The application uses Qt WebEngine's cookie store to create a cookie before navigating to the website.

The cookie is configured with:

```text
Cookie Name: mac_address
Cookie Domain: .3dbharat.com
Cookie Path: /
Secure: True
HttpOnly: False
```

`HttpOnly=False` allows JavaScript executing on the matching website origin to access the cookie.

The application verifies the cookie by executing JavaScript:

```javascript
document.cookie
```

It then compares the returned cookie value with the detected BSSID.

**Important implementation detail:** The cookie is created in the embedded Qt WebEngine browser profile. It is not automatically shared with Chrome, Edge, or other external browsers. The current browser profile is session-based, so cookie persistence after closing the application is not guaranteed.

The client-side verification confirms that JavaScript can read the cookie. It does not independently establish that the website's backend processes or stores the BSSID.

## 10. Windows Registry Configuration

The registry file is located at:

```text
installer/3d_bharat_mac_app.reg
```

It registers application metadata under:

```text
HKEY_CURRENT_USER\Software\3DBharat\MACAddressFetcher
```

To import the registry configuration:

1. Double-click the `.reg` file.
2. Confirm the Windows Registry Editor prompt.
3. Verify the values using PowerShell:

```powershell
reg query "HKCU\Software\3DBharat\MACAddressFetcher"
```

The registry entry is created under the current user's registry hive and does not require administrator privileges.

To remove the entry:

```powershell
reg delete "HKCU\Software\3DBharat\MACAddressFetcher" /f
```

## 11. Building the Windows Executable

PyInstaller is used to package the Python application and its dependencies.

Install PyInstaller:

```powershell
python -m pip install pyinstaller
```

Build the application from the project root:

```powershell
python -m PyInstaller --noconfirm --clean --onedir --name "3D Bharat MAC Address Fetcher" --add-data "config;config" --add-data "license;license" --collect-all PySide6.QtWebEngineCore --collect-all PySide6.QtWebEngineWidgets src/main.py
```

The executable is generated under:

```text
dist/
└── 3D Bharat MAC Address Fetcher/
    ├── 3D Bharat MAC Address Fetcher.exe
    └── _internal/
```

**Important:** Keep the executable and its `_internal` directory together. The executable depends on the bundled Qt libraries, browser resources, configuration, and other supporting files.

## 12. Testing and Verification

The following application checks were performed during development:

| Test | Result |
|---|---|
| Application startup | Passed |
| Wi-Fi BSSID detection | Passed |
| BSSID display in GUI | Passed |
| Embedded website launch | Passed |
| Website loading | Passed |
| Cookie creation | Passed |
| JavaScript cookie visibility | Passed |
| Cookie value comparison | Passed |
| Registry import and verification | Passed |
| Configuration loading | Passed |
| Packaged executable launch | Tested successfully |

Cookie verification produced matching values for the expected and received BSSID.

## 13. Known Limitations

- BSSID detection requires a connected Wi-Fi network and an available wireless interface.
- The application is designed for Windows because it uses `netsh`.
- The cookie belongs to the embedded browser profile and is not automatically available to external browsers.
- JavaScript access to the cookie does not prove backend processing by the website.
- The application requires internet connectivity to load the website.
- Website functionality depends on the availability and compatibility of the external website.

## 14. Deliverables

The submission package should contain:

- Complete Python source code.
- Windows application executable and all supporting files.
- Windows registry `.reg` file.
- Application license and usage notice.
- JSON configuration file.
- Dependency requirements file.
- Project README.
- Windows installer executable, if generated.

## 15. Developer

**Name:** Aniket Khomane  
**Project:** 3D Bharat MAC Address Fetcher  
**Purpose:** Python Developer Technical Assignment  
**Company:** Micro Integrated Semiconductor Systems Pvt. Ltd.
