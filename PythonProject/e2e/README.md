# E2E Test Automation Framework

A comprehensive end-to-end testing framework using pytest and Playwright.

## Structure

```
e2e/
├── conftest.py              # Pytest fixtures and configuration
├── pytest.ini              # Pytest configuration
├── requirements.txt         # Python dependencies
├── setup.py                 # Setup script
├── pages/                   # Page Object Model
│   ├── __init__.py
│   ├── base_page.py        # Base page class
│   └── login_page.py       # Login page specific methods
├── tests/                   # Test files
│   ├── __init__.py
│   └── test_login.py       # Login test cases
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── file_utils.py       # File handling utilities
└── resources/              # Test data and configuration
    ├── config.yaml         # Environment configuration
    ├── locators.yaml       # Element locators
    ├── test_data.yaml      # Test data
    ├── testdata.csv        # CSV test data
    └── create_isi_students.csv # Student test data
```

## Setup

### Prerequisites
- Python 3.8 or higher
- Node.js (for Playwright)

### Installation

1. **Run setup script**
   ```bash
   python setup.py
   ```

2. **Or install manually**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with specific browser
pytest tests/ --browser firefox

# Run headless
pytest tests/ --headless

# Run with markers
pytest tests/ -m smoke
```

## Features

- Page Object Model (POM)
- Data-Driven Testing (YAML/CSV)
- Multiple Browser Support
- Parallel Execution
- Rich Reporting
- Screenshot on Failure
