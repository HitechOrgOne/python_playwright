#!/usr/bin/env python3
"""
Generate HTML reports from test results without Allure CLI
"""
import os
import sys
import subprocess
import webbrowser
from pathlib import Path


def run_tests_with_html_report():
    """Run tests and generate HTML report using multiple methods"""
    
    print("🧪 Running tests with HTML report generation...")
    
    # Method 1: Try pytest-html first (simpler)
    try:
        print("📊 Generating HTML report with pytest-html...")
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", "-v",
            "--html=test-report.html", 
            "--self-contained-html",
            "--alluredir=allure-results",
            "--clean-alluredir"
        ], check=False, capture_output=True, text=True)
        
        print("✅ Tests completed!")
        print(f"📋 HTML Report: {Path('test-report.html').absolute()}")
        
        # Open the report
        if Path("test-report.html").exists():
            webbrowser.open(f"file://{Path('test-report.html').absolute()}")
            
    except Exception as e:
        print(f"❌ Error generating HTML report: {e}")
    
    # Method 2: Try Allure CLI if available
    try:
        print("🎯 Attempting Allure report generation...")
        subprocess.run(["allure", "--version"], check=True, capture_output=True)
        
        # Allure CLI is available
        print("📊 Generating Allure report...")
        subprocess.run([
            "allure", "serve", "allure-results"
        ], check=True)
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ℹ️  Allure CLI not found. Using pytest-html report instead.")
        print("💡 To install Allure CLI:")
        print("   - Download from: https://github.com/allure-framework/allure2/releases")
        print("   - Or use: npm install -g allure-commandline")


def check_requirements():
    """Check if required packages are installed"""
    required_packages = ["pytest", "allure-pytest", "pytest-html"]
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print(f"📦 Install with: pip install {' '.join(missing)}")
        return False
    
    return True


if __name__ == "__main__":
    print("🚀 Test Report Generator")
    print("=" * 40)
    
    if not check_requirements():
        print("Please install missing packages and try again.")
        sys.exit(1)
    
    # Change to e2e directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    run_tests_with_html_report()
