from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def fill_information(self, first_name, last_name, postal_code):
        first = self.wait.until(EC.element_to_be_clickable((By.ID, "first-name")))
        last  = self.wait.until(EC.element_to_be_clickable((By.ID, "last-name")))
        postal = self.wait.until(EC.element_to_be_clickable((By.ID, "postal-code")))

        first.clear()
        first.send_keys(first_name)

        last.clear()
        last.send_keys(last_name)

        postal.clear()
        postal.send_keys(postal_code)

    def click_continue(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.ID, "continue")))
        btn.click()
        self.wait.until(EC.url_contains("checkout-step-two"))
