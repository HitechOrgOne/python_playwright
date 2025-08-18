"""
Setup script for e2e test automation framework
"""
import os
import subprocess
import sys


def install_requirements():
    """Install Python requirements"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True


def install_playwright_browsers():
    """Install Playwright browsers"""
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
        print("✅ Playwright browsers installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Playwright browsers: {e}")
        return False
    return True


def create_directories():
    """Create necessary directories"""
    dirs = [
        "screenshots",
        "videos", 
        "reports",
        "allure-results",
        "logs"
    ]
    
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    
    print("✅ Created necessary directories")


def main():
    """Main setup function"""
    print("🚀 Setting up e2e test automation framework...")
    
    # Install Python requirements
    if not install_requirements():
        sys.exit(1)
    
    # Install Playwright browsers
    if not install_playwright_browsers():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run tests:")
    print("  pytest tests/ -v")
    print("\nTo run with specific browser:")
    print("  pytest tests/ --browser firefox")
    print("\nTo run headless:")
    print("  pytest tests/ --headless")


if __name__ == "__main__":
    main()
