"""
PyCharm configuration helper script
Run this script to configure PyCharm for the e2e project
"""
import os
import sys

def configure_python_path():
    """Configure Python path for the project"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add current directory to Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print(f"Added to Python path: {current_dir}")
    
    # Test imports
    try:
        from pages.login_page import LoginPage
        print("✅ Successfully imported LoginPage")
    except ImportError as e:
        print(f"❌ Failed to import LoginPage: {e}")
    
    try:
        from utils.file_utils import FileUtils
        print("✅ Successfully imported FileUtils")
    except ImportError as e:
        print(f"❌ Failed to import FileUtils: {e}")

def main():
    """Main configuration function"""
    print("Configuring PyCharm project for e2e testing...")
    configure_python_path()
    
    print("\nTo configure PyCharm manually:")
    print("1. Go to File -> Settings -> Project -> Project Structure")
    print("2. Mark the 'e2e' folder as 'Sources Root'")
    print("3. Apply changes and restart PyCharm")
    print("\nOr run tests from the e2e directory with:")
    print("cd e2e && python -m pytest tests/ -v")

if __name__ == "__main__":
    main()
