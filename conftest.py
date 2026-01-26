import pytest
from selenium import webdriver
import tempfile

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()

    # Run with a fresh clean Chrome profile every time
    temp_profile = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_profile}")

    # Incognito helps block Chrome password prompts
    options.add_argument("--incognito")

    # Disable password manager + autofill
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection_enabled": False,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # Remove automation message + popups
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # General stability flags
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
