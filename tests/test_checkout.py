import pytest
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckOutCompletePage
from pages.checkout_overview_page import CheckOutOverviewPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from selenium.webdriver.common.keys import Keys
@pytest.mark.regression
def test_checkout_flow_success(driver):
    cart_page = CartPage(driver)
    checkout_complete_page = CheckOutCompletePage(driver)
    checkout_overview_page = CheckOutOverviewPage(driver)
    checkout_page = CheckoutPage(driver)
    inventory_page = InventoryPage(driver)
    login_page = LoginPage(driver)

    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory_page.add_first_product_to_cart()
    inventory_page.go_to_cart()

    cart_page.click_checkout_button()

    checkout_page.fill_information("ege", "kalenderoglu", "123")
    checkout_page.click_continue()
    print(driver.current_url)

    checkout_overview_page.click_finish()

    assert "thank you" in checkout_complete_page.get_success_message().lower()