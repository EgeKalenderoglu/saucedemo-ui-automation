import pytest
from selenium import webdriver
import tempfile
from datetime import datetime
import os
import logging
from pathlib import Path
from utils.ai_triage import analyze_failure


VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    Path("logs").mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(f"logs/run_{ts}.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )
    logging.info("Test session started")

@pytest.fixture
def driver(request):
    logging.info(f"TEST START: {request.node.nodeid}")
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
    driver.implicitly_wait(10)
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

            analyze_failure(
                test_name=request.node.nodeid,
                exception_message=str(rep.longrepr),
                current_url=driver.current_url,
                page_title=driver.title,
                page_source=driver.page_source,
            )

        if rep and rep.failed:
            logging.error(f"TEST FAILED: {request.node.nodeid}")
        elif rep and rep.passed:
            logging.info(f"TEST PASSED: {request.node.nodeid}")

        driver.quit()
        logging.info(f"TEST END: {request.node.nodeid}")