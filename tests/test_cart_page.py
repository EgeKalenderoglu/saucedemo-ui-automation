import pytest
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

@pytest.mark.regression
def test_cart_page_contains_item_after_adding(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory_page.add_first_product_to_cart()
    inventory_page.go_to_cart()

    assert cart_page.get_cart_items_count() == 1
