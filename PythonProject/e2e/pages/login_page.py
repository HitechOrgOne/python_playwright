"""
Login page object model for Playwright
"""
from pathlib import Path
from playwright.sync_api import Page, expect

from e2e.utils.file_utils import FileUtils
from .base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        locators = Path(__file__).parent.parent / "locators" / "login_page_locators.yaml"

        # Define Locator objects directly
        self.username_field = page.locator(FileUtils.get_locator("login_page", "username_field", locators))
        self.password_field = page.locator(FileUtils.get_locator("login_page", "password_field", locators))
        self.login_button   = page.locator(FileUtils.get_locator("login_page", "login_button", locators))
        self.error_message  = page.locator(FileUtils.get_locator("login_page", "error_message", locators))
        self.logout_button  = page.locator(FileUtils.get_locator("login_page", "logout_button", locators))

    def enter_username(self, username: str):
        """Enter username"""
        self.username_field.fill(username)

    def enter_password(self, password: str):
        """Enter password"""
        self.password_field.fill(password)

    def click_login(self):
        """Click login button"""
        self.login_button.click()

    def login(self, username: str, password: str):
        """Complete login process"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Get error message text"""
        return self.error_message.inner_text()

    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.error_message.is_visible()

    def is_welcome_message_visible(self) -> bool:
        """Check if welcome message is visible after successful login"""
        return self.welcome_message.is_visible()

    def logout(self):
        """Perform logout"""
        self.logout_button.click()

    def wait_for_login_page_load(self):
        """Wait for login page to fully load"""
        expect(self.username_field).to_be_visible()
        expect(self.password_field).to_be_visible()
        expect(self.login_button).to_be_visible()

    def is_login_form_visible(self) -> bool:
        """Check if login form is visible"""
        return (self.username_field.is_visible() and
                self.password_field.is_visible() and
                self.login_button.is_visible())
