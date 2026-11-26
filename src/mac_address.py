
import re
import subprocess


MAC_PATTERN = re.compile(
    r"(?:[0-9A-F]{2}[:-]){5}[0-9A-F]{2}",
    re.IGNORECASE
)


def get_connected_wifi_bssid() -> str:
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True,
            text=True,
            errors="replace",
            timeout=10
        )

    except FileNotFoundError:
        raise RuntimeError("Windows netsh command was not found.")

    except subprocess.TimeoutExpired:
        raise RuntimeError("Wi-Fi detection command timed out.")

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or "Unable to retrieve Wi-Fi information."
        )

    output = result.stdout

    # Separate individual Wi-Fi interface sections.
    interfaces = re.split(
        r"(?=^\s*Name\s*:)",
        output,
        flags=re.IGNORECASE | re.MULTILINE
    )

    for interface in interfaces:

        # Only consider connected Wi-Fi interfaces.
        state_match = re.search(
            r"^\s*State\s*:\s*connected\s*$",
            interface,
            re.IGNORECASE | re.MULTILINE
        )

        if not state_match:
            continue

        bssid_match = re.search(
            r"^\s*BSSID\s*:\s*([0-9A-F:-]+)",
            interface,
            re.IGNORECASE | re.MULTILINE
        )

        if bssid_match:
            mac_address = bssid_match.group(1).upper()
            
            if MAC_PATTERN.fullmatch(mac_address):
                return mac_address.replace("-", ":")

    raise RuntimeError(
        "No connected Wi-Fi network found or BSSID unavailable."
    )
