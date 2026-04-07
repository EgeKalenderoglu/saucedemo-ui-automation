# SauceDemo UI Automation Framework

A UI test automation framework built with Python, Selenium, and Pytest using the Page Object Model (POM) design pattern. Features an AI-assisted failure triage layer that automatically analyzes test failures using the Claude API.

Target Website: https://www.saucedemo.com/

---

## Tech Stack

- Python 3.12
- Selenium WebDriver
- Pytest
- Google Chrome + ChromeDriver
- Anthropic Claude API (AI failure triage)

---

## Project Structure
```text
saucedemo-ui-automation/
│
├── pages/                          # Page Objects (UI actions + locators)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── checkout_overview_page.py
│   └── checkout_complete_page.py
│
├── tests/                          # Test cases
│   ├── test_login.py
│   ├── test_cart.py
│   └── test_checkout.py
│
├── utils/                          # Utilities
│   └── ai_triage.py                # AI-assisted failure analysis
│
├── conftest.py                     # Pytest fixtures (driver setup + logging)
├── pytest.ini                      # Pytest markers config
├── requirements.txt                # Project dependencies
├── .env.example                    # Environment variable template
└── README.md
```

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/EgeKalenderoglu/saucedemo-ui-automation.git
cd saucedemo-ui-automation
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**
```bash
cp .env.example .env
```
Then open `.env` and add your Anthropic API key:
```bash
ANTHROPIC_API_KEY=your-key-here
```
---

## How To Run Tests

Run all tests:
```bash
pytest -v
```

Run only smoke tests:
```bash
pytest -m smoke -v
```

Run only regression tests:
```bash
pytest -m regression -v
```

Run a single test file:
```bash
pytest tests/test_checkout.py -v
```

---

## What This Framework Tests

### Login Tests
- Successful login redirects to inventory page
- Wrong password displays error message

### Cart Tests
- Adding a product updates the cart badge count
- Cart page contains the correct item after adding

### Checkout Tests
- Full checkout flow: login → add item → go to cart → fill info → finish

---

## AI-Assisted Failure Triage

When a test fails, the framework automatically:

1. Captures a screenshot, page source, and current URL
2. Sends the failure context to the Claude API for analysis
3. Saves a structured JSON diagnosis to the `artifacts/` folder

Example triage output:
```json
{
  "failure_type": "assertion_failure",
  "confidence": "high",
  "likely_cause": "The expected text was not found on the page.",
  "suggested_fix": "Verify the assertion matches the actual page content.",
  "summary": "The test failed because the assertion condition was not met. Check the locator or expected value."
}
```

Failure types identified: `locator_issue`, `timeout`, `assertion_failure`, `navigation_error`, `application_bug`, `environment_issue`

---

## Failure Artifacts

When a test fails, the following are saved to the `artifacts/` folder:

- Screenshot (`.png`)
- Page source (`.html`)
- Current URL + page title (`.txt`)
- AI triage analysis (`.json`)

---

## Test Reports

An HTML report is automatically generated on every test run:
```bash
open reports/report.html
```

---

## Logging

Every test run generates a timestamped log file in the `logs/` folder recording test start, result, and end time for every test.

---

## Author

Ege Kalenderoglu 