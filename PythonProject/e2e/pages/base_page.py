"""
Base page class for Playwright page object model using Locators
"""
from playwright.sync_api import Page, expect, Locator


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # --- Navigation ---

    def navigate_to(self, url: str):
        """Navigate to the specified URL"""
        self.page.goto(url)

    # --- Element interactions using Locators ---

    def click(self, element: Locator):
        """Click on element (auto-waits)"""
        element.click()

    def fill_text(self, element: Locator, text: str):
        """Fill text in input field (auto-waits)"""
        element.fill(text)

    def type_text(self, element: Locator, text: str):
        """Type text character by character (auto-waits)"""
        element.type(text)

    def get_text(self, element: Locator) -> str:
        """Get inner text of element (auto-waits)"""
        return element.inner_text()

    def is_visible(self, element: Locator) -> bool:
        """Check if element is visible (without auto-waiting)"""
        return element.is_visible(timeout=0)

    def is_enabled(self, element: Locator) -> bool:
        """Check if element is enabled (without auto-waiting)"""
        return element.is_enabled(timeout=0)

    def wait_for_element(self, element: Locator, timeout: int = 10000):
        """Wait for element to be visible"""
        element.wait_for(state="visible", timeout=timeout)

    # --- Page-level methods ---

    def wait_for_url(self, url: str, timeout: int = 10000):
        """Wait for URL to match"""
        self.page.wait_for_url(url, timeout=timeout)

    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url

    def get_title(self) -> str:
        """Get page title"""
        return self.page.title()

    def scroll_to_element(self, element: Locator):
        """Scroll to element"""
        element.scroll_into_view_if_needed()

    def select_option(self, element: Locator, value: str):
        """Select option from dropdown"""
        element.select_option(value)

    def upload_file(self, element: Locator, file_path: str):
        """Upload file"""
        element.set_input_files(file_path)

    def take_screenshot(self, path: str = None):
        """Take screenshot"""
        if path:
            self.page.screenshot(path=path)
        else:
            return self.page.screenshot()

    def press_key(self, element: Locator, key: str):
        """Press key on element"""
        element.press(key)

    def hover(self, element: Locator):
        """Hover over element"""
        element.hover()

    def double_click(self, element: Locator):
        """Double click on element"""
        element.dblclick()

    def right_click(self, element: Locator):
        """Right click on element"""
        element.click(button="right")

    def get_attribute(self, element: Locator, attribute: str) -> str:
        """Get attribute value of element"""
        return element.get_attribute(attribute)

    def set_viewport_size(self, width: int, height: int):
        """Set viewport size"""
        self.page.set_viewport_size({"width": width, "height": height})
