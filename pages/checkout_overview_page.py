from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckOutOverviewPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_finish(self):
        self.wait.until(EC.url_contains("checkout-step-two"))
        self.wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()
