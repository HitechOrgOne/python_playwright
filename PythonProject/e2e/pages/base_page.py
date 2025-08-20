"""
Base page class for Playwright page object model using Locators
"""
from playwright.sync_api import Page, expect, Locator

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # No change needed here; page.goto is the correct way to navigate.
    def navigate_to(self, url: str):
        """Navigate to the specified URL"""
        self.page.goto(url)

    # --- Use Locator for element interactions ---

    def click(self, selector: str):
        """Click on element using selector (auto-waits)"""
        self.page.locator(selector).click()

    def fill_text(self, selector: str, text: str):
        """Fill text in input field (auto-waits)"""
        self.page.fill(selector, text)

    def type_text(self, selector: str, text: str):
        """Type text character by character (auto-waits)"""
        self.page.type(selector, text)

    def get_text(self, selector: str) -> str:
        """Get inner text of element (auto-waits)"""
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        """Check if element is visible (without auto-waiting)"""
        # Using a timeout of 0 to check the current state instantly.
        return self.page.locator(selector).is_visible(timeout=0)

    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled (without auto-waiting)"""
        return self.page.locator(selector).is_enabled(timeout=0)

    # Note: With auto-waiting on other methods, explicit waits are less common.
    def wait_for_element(self, selector: str, timeout: int = 10000):
        """Wait for element to be visible"""
        # Using the locator's wait_for method is more specific.
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)

    # No change needed here; page.wait_for_url is correct.
    def wait_for_url(self, url: str, timeout: int = 10000):
        """Wait for URL to match"""
        self.page.wait_for_url(url, timeout=timeout)

    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url

    def get_title(self) -> str:
        """Get page title"""
        return self.page.title()

    def scroll_to_element(self, selector: str):
        """Scroll to element"""
        self.page.locator(selector).scroll_into_view_if_needed()

    def select_option(self, selector: str, value: str):
        """Select option from dropdown"""
        self.page.locator(selector).select_option(value)

    # Note: `set_input_files` is a page-level method, not a locator method.
    def upload_file(self, selector: str, file_path: str):
        """Upload file"""
        self.page.set_input_files(selector, file_path)

    # Note: `screenshot` is a page-level method.
    def take_screenshot(self, path: str = None):
        """Take screenshot"""
        if path:
            self.page.screenshot(path=path)
        else:
            return self.page.screenshot()

    def press_key(self, selector: str, key: str):
        """Press key on element"""
        self.page.locator(selector).press(key)

    def hover(self, selector: str):
        """Hover over element"""
        self.page.locator(selector).hover()

    def double_click(self, selector: str):
        """Double click on element"""
        self.page.locator(selector).dblclick()

    def right_click(self, selector: str):
        """Right click on element"""
        self.page.locator(selector).click(button="right")

    def get_attribute(self, selector: str, attribute: str) -> str:
        """Get attribute value of element"""
        return self.page.locator(selector).get_attribute(attribute)

    # No change needed here; set_viewport_size is a page-level method.
    def set_viewport_size(self, width: int, height: int):
        """Set viewport size"""
        self.page.set_viewport_size({"width": width, "height": height})
