import os
import sys

def create_project_structure(project_name="test_automation"):
    """
    Creates a test automation project folder structure inside existing project
    """
    
    print(f"Creating test automation structure in: {project_name}/")
    
    # Define the folder structure
    folders = [
        project_name,
        os.path.join(project_name, "pages"),
        os.path.join(project_name, "resources"),
        os.path.join(project_name, "tests"),
        os.path.join(project_name, "utils"),
    ]
    
    # Files to create
    files = [
        os.path.join(project_name, "conftest.py"),
        os.path.join(project_name, "pytest.ini"),
        os.path.join(project_name, "requirements.txt"),
        os.path.join(project_name, "pages", "base_page.py"),
        os.path.join(project_name, "pages", "login_page.py"),
        os.path.join(project_name, "resources", "login_page_locators.yaml"),
        os.path.join(project_name, "resources", "test_data.yaml"),
        os.path.join(project_name, "resources", "config.yaml"),
        os.path.join(project_name, "tests", "test_login.py"),
        os.path.join(project_name, "utils", "file_utils.py"),
        os.path.join(project_name, "utils", "__init__.py"),
    ]
    
    # Create folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Created folder: {folder}")
    
    # Create files with test automation specific content
    file_contents = {
        os.path.join(project_name, "conftest.py"): '''"""
Pytest configuration and shared fixtures
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def browser():
    """Browser fixture for selenium tests"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Remove for visible browser
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()


@pytest.fixture
def config():
    """Configuration fixture"""
    return {
        "base_url": "https://example.com",
        "timeout": 10
    }
''',
        os.path.join(project_name, "pytest.ini"): '''[tool:pytest]
addopts = -v --tb=short --strict-markers
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    smoke: smoke tests
    regression: regression tests
    ui: UI tests
    api: API tests
''',
        os.path.join(project_name, "requirements.txt"): '''# Test automation dependencies
selenium>=4.15.0
pytest>=7.4.0
pytest-html>=3.2.0
pyyaml>=6.0.1
requests>=2.31.0
allure-pytest>=2.13.2
webdriver-manager>=4.0.1
''',
        os.path.join(project_name, "pages", "base_page.py"): '''"""
Base page class with common methods
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import yaml
import os


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.locators = self._load_locators()
    
    def _load_locators(self):
        """Load locators from YAML file"""
        locator_file = os.path.join(os.path.dirname(__file__), '..', 'resources', 'login_page_locators.yaml')
        with open(locator_file, 'r') as file:
            return yaml.safe_load(file)
    
    def find_element(self, locator):
        """Find element using locator tuple (By.*, 'value')"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def click(self, locator):
        """Click on element"""
        element = self.find_element(locator)
        element.click()
    
    def enter_text(self, locator, text):
        """Enter text into element"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text from element"""
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            element = self.find_element(locator)
            return element.is_displayed()
        except:
            return False
''',
        os.path.join(project_name, "pages", "login_page.py"): '''"""
Login page object model
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        
        # Locators
        self.username_field = (By.ID, "username")
        self.password_field = (By.ID, "password")
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.error_message = (By.CLASS_NAME, "error-message")
    
    def enter_username(self, username):
        """Enter username"""
        self.enter_text(self.username_field, username)
    
    def enter_password(self, password):
        """Enter password"""
        self.enter_text(self.password_field, password)
    
    def click_login(self):
        """Click login button"""
        self.click(self.login_button)
    
    def login(self, username, password):
        """Complete login process"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def get_error_message(self):
        """Get error message text"""
        return self.get_text(self.error_message)
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_visible(self.error_message)
''',
        os.path.join(project_name, "resources", "login_page_locators.yaml"): '''# Page locators
login_page:
  username_field:
    by: "id"
    value: "username"
  password_field:
    by: "id"
    value: "password"
  login_button:
    by: "xpath"
    value: "//button[@type='submit']"
  error_message:
    by: "class_name"
    value: "error-message"

home_page:
  welcome_message:
    by: "xpath"
    value: "//h1[contains(text(), 'Welcome')]"
  logout_button:
    by: "id"
    value: "logout"
''',
        os.path.join(project_name, "resources", "test_data.yaml"): '''# Test data for automation
users:
  valid_user:
    username: "testuser@example.com"
    password: "validpassword123"
  
  invalid_user:
    username: "invalid@example.com"
    password: "wrongpassword"

  empty_credentials:
    username: ""
    password: ""

urls:
  login_page: "https://example.com/login"
  home_page: "https://example.com/dashboard"
  
error_messages:
  invalid_credentials: "Invalid username or password"
  empty_username: "Username is required"
  empty_password: "Password is required"

timeouts:
  implicit_wait: 10
  explicit_wait: 15
  page_load_timeout: 30
''',
        os.path.join(project_name, "resources", "config.yaml"): '''# Configuration settings
browser:
  name: "chrome"  # chrome, firefox, edge
  headless: false
  maximize: true

environment:
  base_url: "https://example.com"
  api_base_url: "https://api.example.com"

timeouts:
  implicit_wait: 10
  explicit_wait: 15
  page_load_timeout: 30

reporting:
  screenshot_on_failure: true
  video_recording: false
  allure_results_dir: "allure-results"

database:
  host: "localhost"
  port: 5432
  name: "test_db"
  username: "test_user"
  password: "test_pass"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "test_automation.log"
''',
        os.path.join(project_name, "tests", "test_login.py"): '''"""
Login functionality tests
"""
import pytest
import yaml
import os
import sys

# Add pages to Python path for importing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pages.login_page import LoginPage


class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, browser):
        """Setup for each test"""
        self.driver = browser
        self.login_page = LoginPage(self.driver)
        
        # Load test data
        test_data_file = os.path.join(os.path.dirname(__file__), '..', 'resources', 'test_data.yaml')
        with open(test_data_file, 'r') as file:
            self.test_data = yaml.safe_load(file)
        
        # Navigate to login page
        self.driver.get(self.test_data['urls']['login_page'])
    
    @pytest.mark.smoke
    def test_valid_login(self):
        """Test login with valid credentials"""
        user_data = self.test_data['users']['valid_user']
        
        self.login_page.login(
            user_data['username'], 
            user_data['password']
        )
        
        # Assert successful login (modify based on your app)
        assert self.driver.current_url == self.test_data['urls']['home_page']
    
    @pytest.mark.regression
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        user_data = self.test_data['users']['invalid_user']
        
        self.login_page.login(
            user_data['username'], 
            user_data['password']
        )
        
        # Assert error message is displayed
        assert self.login_page.is_error_displayed()
        error_text = self.login_page.get_error_message()
        assert self.test_data['error_messages']['invalid_credentials'] in error_text
    
    @pytest.mark.regression
    def test_empty_credentials(self):
        """Test login with empty credentials"""
        user_data = self.test_data['users']['empty_credentials']
        
        self.login_page.login(
            user_data['username'], 
            user_data['password']
        )
        
        # Assert error message for empty fields
        assert self.login_page.is_error_displayed()
    
    @pytest.mark.ui
    def test_username_field_visible(self):
        """Test username field is visible"""
        assert self.login_page.is_element_visible(self.login_page.username_field)
    
    @pytest.mark.ui
    def test_password_field_visible(self):
        """Test password field is visible"""
        assert self.login_page.is_element_visible(self.login_page.password_field)
    
    @pytest.mark.ui
    def test_login_button_visible(self):
        """Test login button is visible"""
        assert self.login_page.is_element_visible(self.login_page.login_button)
''',
        os.path.join(project_name, "utils", "file_utils.py"): '''"""
File utility functions for test automation
"""
import yaml
import json
import csv
import os
from typing import Dict, Any, List


class FileUtils:
    
    @staticmethod
    def load_yaml(file_path: str) -> Dict[Any, Any]:
        """Load YAML file and return data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file {file_path}: {e}")
    
    @staticmethod
    def save_yaml(data: Dict[Any, Any], file_path: str) -> None:
        """Save data to YAML file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False, indent=2)
    
    @staticmethod
    def load_json(file_path: str) -> Dict[Any, Any]:
        """Load JSON file and return data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON file {file_path}: {e}")
    
    @staticmethod
    def save_json(data: Dict[Any, Any], file_path: str) -> None:
        """Save data to JSON file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_csv(file_path: str) -> List[Dict[str, str]]:
        """Load CSV file and return list of dictionaries"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {file_path}")
    
    @staticmethod
    def create_directory(directory_path: str) -> None:
        """Create directory if it doesn't exist"""
        os.makedirs(directory_path, exist_ok=True)
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if file exists"""
        return os.path.isfile(file_path)
    
    @staticmethod
    def get_project_root() -> str:
        """Get project root directory"""
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    @staticmethod
    def get_resource_path(filename: str) -> str:
        """Get full path to resource file"""
        project_root = FileUtils.get_project_root()
        return os.path.join(project_root, 'resources', filename)
'''
    }
    
    # Create files with content
    for file_path, content in file_contents.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created file: {file_path}")
    
    # Create empty __init__.py file for utils
    init_file = os.path.join(project_name, "utils", "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('')
        print(f"✅ Created file: {init_file}")
    
    print(f"\n🎉 SUCCESS! Test automation structure created!")
    print(f"📁 Created inside your existing project: {project_name}/")
    
    structure_display = f"""
📋 Structure created:
{project_name}/
├── conftest.py
├── pytest.ini  
├── requirements.txt
├── pages/
│   ├── base_page.py
│   └── login_page.py
├── resources/
│   ├── login_page_locators.yaml
│   ├── test_data.yaml
│   └── config.yaml
├── tests/
│   └── test_login.py
└── utils/
    ├── file_utils.py
    └── __init__.py
    """
    
    print(structure_display)
    
    print(f"🔧 Next steps:")
    print(f"1. In PyCharm terminal, install dependencies:")
    print(f"   pip install -r {project_name}/requirements.txt")
    print(f"2. Install chromedriver manager:")
    print(f"   pip install webdriver-manager")
    print(f"3. Run your tests:")
    print(f"   pytest {project_name}/tests/ -v")
    print(f"4. Mark {project_name} as Sources Root in PyCharm:")
    print(f"   Right-click {project_name} → Mark Directory as → Sources Root")


if __name__ == "__main__":
    print("🚀 Test Automation Structure Creator")
    print("=" * 40)
    print("This will create a test automation folder inside your current project.")
    print()
    
    # Get current working directory
    current_dir = os.getcwd()
    print(f"📍 Current location: {current_dir}")
    print()
    
    # Get project name
    project_name = input("📝 Enter folder name for test automation (default: 'test_automation'): ").strip()
    if not project_name:
        project_name = "test_automation"
    
    # Replace spaces and special characters
    project_name = project_name.replace(' ', '_').replace('-', '_')
    
    # Check if folder already exists
    if os.path.exists(project_name):
        overwrite = input(f"⚠️  Folder '{project_name}' already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite not in ['y', 'yes']:
            print("❌ Operation cancelled.")
            exit()
    
    print(f"\n🔨 Creating test automation structure in: {project_name}/")
    print("-" * 50)
    
    create_project_structure(project_name)
