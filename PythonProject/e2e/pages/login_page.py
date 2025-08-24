"""
Login page object model for Playwright using clean Page Object Model
"""
from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):

    
    # Selectors stored as class-level constants
    USERNAME_SELECTOR = "#user-name"
    PASSWORD_SELECTOR = "#password"
    LOGIN_BUTTON_SELECTOR = "#login-button"
    ERROR_MESSAGE_SELECTOR = "[data-test='error']"
    LOGOUT_BUTTON_SELECTOR = "#logout_sidebar_link"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Initialize Locator objects once
        self.username_field = page.locator(self.USERNAME_SELECTOR)
        self.password_field = page.locator(self.PASSWORD_SELECTOR)
        self.login_button = page.locator(self.LOGIN_BUTTON_SELECTOR)
        self.error_message = page.locator(self.ERROR_MESSAGE_SELECTOR)
        self.logout_button = page.locator(self.LOGOUT_BUTTON_SELECTOR)

    # Page actions
    def enter_username(self, username: str):
        self.username_field.fill(username)

    def enter_password(self, password: str):
        self.password_field.fill(password)

    def click_login(self):
        self.login_button.click()

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        return self.error_message.inner_text()

    def is_error_displayed(self) -> bool:
        return self.error_message.is_visible()

    def logout(self):
        self.logout_button.click()

    def wait_for_login_page_load(self):
        expect(self.username_field).to_be_visible()
        expect(self.password_field).to_be_visible()
        expect(self.login_button).to_be_visible()

    def is_login_form_visible(self) -> bool:
        return (
            self.username_field.is_visible() and
            self.password_field.is_visible() and
            self.login_button.is_visible()
        )
