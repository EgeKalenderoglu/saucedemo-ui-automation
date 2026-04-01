from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_cart_items_count(self):
        items = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "cart_item")))
        return len(items)

    def click_checkout_button(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
    