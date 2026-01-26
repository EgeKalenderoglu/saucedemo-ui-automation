# SauceDemo UI Automation Framework

This project is a UI test automation framework built with Python + Selenium + Pytest using the Page Object Model (POM) design pattern.

Target Website: https://www.saucedemo.com/

---

## Tech Stack
- Python 3.12
- Selenium WebDriver
- Pytest
- Google Chrome + ChromeDriver

---

## Project Structure

saucedemo-ui-automation/
│
├── pages/                      # Page Objects (UI actions + locators)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── checkout_overview_page.py
│   └── checkout_complete_page.py
│
├── tests/                      # Test cases
│   ├── test_login.py
│   ├── test_cart.py
│   └── test_checkout.py
│
├── conftest.py                 # Pytest fixtures (driver setup)
├── pytest.ini                  # Pytest markers config
└── README.md

---

## What This Framework Tests

### Login Tests
- Successful login
- Wrong password shows an error message

### Cart Tests
- Add product to cart
- Cart badge shows correct count

### Checkout Tests
- Full checkout flow:
  login → add item → go to cart → checkout → fill info → continue → finish

---

## How To Run Tests

Run all tests:
    pytest -q

Run only smoke tests:
    pytest -m smoke -q

Run only regression tests:
    pytest -m regression -q

Run a single test file:
    pytest tests/test_checkout.py -q

---

## Notes
- Tests are written using the Page Object Model (POM) structure.
- conftest.py handles the browser setup/teardown using Pytest fixtures.
- pytest.ini registers custom markers so Pytest does not show warnings.

---

## Author
Ege Kalenderoglu
