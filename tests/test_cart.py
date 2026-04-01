import pytest
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from conftest import VALID_PASSWORD, VALID_USERNAME
@pytest.mark.regression
def test_add_to_cart_shows_correct_count(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    login_page.open()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    inventory_page.add_first_product_to_cart()
    cart_count = inventory_page.get_cart_count()

    assert cart_count == "1"