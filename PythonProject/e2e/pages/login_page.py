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
        self.welcome_message = None
        locators = Path(__file__).parent.parent / "locators" / "login_page_locators.yaml"
        self.username_field = FileUtils.get_locator("login_page", "username_field", locators)
        self.password_field = FileUtils.get_locator("login_page", "password_field", locators)
        self.login_button = FileUtils.get_locator("login_page", "login_button", locators)
        self.error_message = FileUtils.get_locator("login_page", "error_message", locators)
        self.logout_button = FileUtils.get_locator("login_page", "logout_button", locators)

    def enter_username(self, username: str):
        """Enter username"""
        self.fill_text(self.username_field, username)
    
    def enter_password(self, password: str):
        """Enter password"""
        self.fill_text(self.password_field, password)
    
    def click_login(self):
        """Click login button"""
        self.click(self.login_button)
    
    def login(self, username: str, password: str):
        """Complete login process"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def get_error_message(self) -> str:
        """Get error message text"""
        return self.get_text(self.error_message)
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_visible(self.error_message)
    
    def is_welcome_message_visible(self) -> bool:
        """Check if welcome message is visible after successful login"""
        return self.is_visible(self.welcome_message)
    
    def logout(self):
        """Perform logout"""
        self.click(self.logout_button)
    
    def wait_for_login_page_load(self):
        """Wait for login page to fully load"""
        self.wait_for_element(self.username_field)
        self.wait_for_element(self.password_field)
        self.wait_for_element(self.login_button)
    
    def is_login_form_visible(self) -> bool:
        """Check if login form is visible"""
        return (self.is_visible(self.username_field) and 
                self.is_visible(self.password_field) and 
                self.is_visible(self.login_button))
