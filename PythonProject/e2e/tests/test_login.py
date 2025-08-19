import pytest
from e2e.pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_valid_user(page, base_url, app_config):
    """
    Smoke test: verify a valid user can log in successfully.
    """
    login_page = LoginPage(page)
    login_page.navigate_to(f"{base_url}")
    username = app_config.get("username")
    password = app_config.get("password")
    login_page.login(username, password)
    assert page.url == f"{base_url}/inventory.html", "Login failed, did not redirect to dashboard."

@pytest.mark.skip(reason="This test is currently being refactored and is broken.")
@pytest.mark.regression
def test_login_invalid_password(page, base_url, app_config):
    """
    Regression test: verify login fails with invalid password.
    """
    login_page = LoginPage(page)
    login_page.navigate_to(f"{base_url}/login")
    login_page.login(app_config.get("username"), "<PASSWORD>")
    assert page.url == test_data["expected_url"]
