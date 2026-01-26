from calendar import error

import pytest
from selenium.webdriver.common.by import By

@pytest.mark.smoke
def test_successful_login(driver):
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    assert "inventory" in driver.current_url

@pytest.mark.regression
def test_login_wrong_passwords_shows_error(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()

    error_text = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text

    assert "do not match" in error_text.lower()
