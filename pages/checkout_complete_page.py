from selenium.webdriver.common.by import By

class CheckOutCompletePage:
    def __init__(self, driver):
        self.driver = driver

    def get_success_message(self):
        return self.driver.find_element(By.CLASS_NAME, "complete-header").text