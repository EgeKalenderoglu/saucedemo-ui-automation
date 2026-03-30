import pytest
from pages.login_page import LoginPage

@pytest.mark.smoke
def test_successful_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    assert "inventory" in driver.current_url


@pytest.mark.regression
def test_login_wrong_passwords_shows_error(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user","wrong_password")
    error_text = login_page.get_error_message()
    assert "do not match" in error_text.lower()
