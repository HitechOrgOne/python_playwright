import pytest
import os
from pathlib import Path
from dotenv import dotenv_values
from e2e.utils.file_utils import FileUtils
import allure
from e2e.constants import  ENV_FILE_NAME
from utils.config import get_env_variable

# Resolve project root dynamically (conftest.py lives inside e2e/)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

@pytest.fixture(scope="session")
def app_config():
    """
    Loads test configuration:
    - First from .env file (for local/dev use)
    - Falls back to environment variables (for CI/CD)
    """
    e2e_root = Path(__file__).resolve().parent
    env_test_path = e2e_root / ENV_FILE_NAME
    config = {}
    if env_test_path.exists():
        # Load from .env
        config = dotenv_values(env_test_path)
    
    # Fallback to system environment (CI/CD case)
    config = {
        **config,
        "username": config.get("username") or os.getenv("TEST_USERNAME"),
        "password": config.get("password") or os.getenv("TEST_PASSWORD"),
    }
    return config

@pytest.fixture(scope="session")
def base_url(app_config):
    url = os.getenv("BASE_URL") or app_config.get("base_url")
    if not url:
        url = "https://example.com"
    return url

@pytest.fixture(scope="session")
def playwright_action_timeout(app_config):
    """
    Global Playwright action timeout (in ms).
    - Reads from env var PLAYWRIGHT_ACTION_TIMEOUT
    - Falls back to .env.test key playwright_action_timeout
    - Defaults to 5000 ms
    """
    return int(
        os.getenv("PLAYWRIGHT_ACTION_TIMEOUT")
        or app_config.get("playwright_action_timeout", 5000)
    )

@pytest.fixture(scope="session")
def playwright_navigation_timeout(app_config):
    """Global Playwright navigation timeout (ms)."""
    return int(
        os.getenv("PLAYWRIGHT_NAVIGATION_TIMEOUT")
        or app_config.get("playwright_navigation_timeout", 60000)
    )

@pytest.fixture(scope="session")
def playwright_test_timeout(app_config):
    """Global Pytest test timeout (ms)."""
    return int(
        os.getenv("PLAYWRIGHT_TEST_TIMEOUT")
        or app_config.get("playwright_test_timeout", 60000)
    )

@pytest.fixture(scope="session")
def all_test_data():
    csv_path = PROJECT_ROOT / "e2e" / "resources" / "testdata.csv"
    return FileUtils.read_csv(csv_path)

@pytest.fixture
def test_data(request, all_test_data):
    """
    Return only the row that matches the current test function name.
    If not found, show all available test_case_name values from the CSV.
    """
    test_name = request.function.__name__
    for row in all_test_data:
        if row.get("test_case_name") == test_name:
            return row

    available = [row.get("test_case_name") for row in all_test_data]
    raise ValueError(
        f"No test data found for '{test_name}'. "
        f"Available test_case_name values in CSV: {available}"
    )

@pytest.fixture(autouse=True)
def apply_playwright_timeouts(page, playwright_action_timeout, playwright_navigation_timeout, playwright_test_timeout, request):
    page.set_default_timeout(playwright_action_timeout)
    page.set_default_navigation_timeout(playwright_navigation_timeout)
    request.node.add_marker(pytest.mark.timeout(playwright_test_timeout / 1000))

    yield
    # No cleanup needed


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to attach screenshot and video on failure.
    """
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        page = item.funcargs.get("page", None)
        if page:
            # Screenshot
            screenshot_path = PROJECT_ROOT / f"screenshot_{item.name}.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            allure.attach.file(
                str(screenshot_path),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            # Video (only if Playwright was configured for recording)
            try:
                if page.video:
                    video_path = page.video.path()
                    allure.attach.file(
                        str(video_path),
                        name="video",
                        attachment_type=allure.attachment_type.MP4
                    )
            except Exception:
                pass
