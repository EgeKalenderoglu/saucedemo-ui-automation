import pytest
from selenium import webdriver
import tempfile
from datetime import datetime
import os

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture
def driver(request):
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
    try:
        yield driver
    finally:
        rep = getattr(request.node, "rep_call", None)
        if rep and rep.failed:
            os.makedirs("artifacts", exist_ok=True)
            test_name = request.node.nodeid.replace("/", "_").replace("::", "__")
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"artifacts/{test_name}_{ts}.png"
            html_path = f"artifacts/{test_name}_{ts}.html"

            driver.save_screenshot(screenshot_path)

            info_path = f"artifacts/{test_name}_{ts}.txt"
            with open(info_path, "w", encoding="utf-8") as f:
                f.write(f"URL: {driver.current_url}\n")
                f.write(f"TITLE: {driver.title}\n")

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
        driver.quit()
