
import json
import sys
from pathlib import Path


def get_base_directory():
    """
    Returns the project directory during development
    or the temporary extraction directory when packaged.
    """
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)

    return Path(__file__).resolve().parent.parent


def load_config():
    config_path = get_base_directory() / "config" / "config.json"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    try:
        with config_path.open("r", encoding="utf-8") as file:
            config = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON configuration: {error}"
        ) from error

    # Validate required configuration values
    required_keys = [
        ("application", "name"),
        ("application", "version"),
        ("application", "company"),
        ("website", "url"),
        ("cookie", "name"),
        ("cookie", "domain"),
        ("cookie", "path"),
        ("cookie", "secure"),
        ("cookie", "http_only"),
    ]

    for section, key in required_keys:
        if section not in config or key not in config[section]:
            raise ValueError(
                f"Missing configuration: {section}.{key}"
            )

    return config


CONFIG = load_config()
