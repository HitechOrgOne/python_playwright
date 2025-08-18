#!/usr/bin/env python3
"""
Test runner script for e2e tests
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime


def run_tests(args):
    """Run pytest with specified arguments"""
    
    # Base pytest command
    cmd = [sys.executable, "-m", "pytest", "tests/"]
    
    # Add verbosity
    if args.verbose:
        cmd.append("-v")
    
    # Add browser selection
    if args.browser:
        cmd.extend(["--browser", args.browser])
    
    # Add headless mode
    if args.headless:
        cmd.append("--headless")
    
    # Add parallel execution
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])
    
    # Add markers
    if args.markers:
        cmd.extend(["-m", args.markers])
    
    # Add HTML report
    if args.html_report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"reports/report_{timestamp}.html"
        cmd.extend(["--html", report_file, "--self-contained-html"])
        print(f"HTML report will be saved to: {report_file}")
        
        # Always add allure results too
        cmd.extend(["--alluredir", "allure-results", "--clean-alluredir"])
    
    # Add specific test file
    if args.test_file:
        cmd = [sys.executable, "-m", "pytest", f"tests/{args.test_file}"]
    
    # Add allure reporting
    if args.allure:
        cmd.extend(["--alluredir", "allure-results"])
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="E2E Test Runner")
    
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-b", "--browser", choices=["chromium", "firefox", "webkit"], 
                       default="chromium", help="Browser to use")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("-n", "--parallel", type=int, help="Number of parallel workers")
    parser.add_argument("-m", "--markers", help="Test markers to run (e.g., smoke, regression)")
    parser.add_argument("--html-report", action="store_true", help="Generate HTML report")
    parser.add_argument("--allure", action="store_true", help="Generate Allure report")
    parser.add_argument("-f", "--test-file", help="Specific test file to run")
    
    # Pre-defined test suites
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--regression", action="store_true", help="Run regression tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    
    # Handle pre-defined suites
    if args.smoke:
        args.markers = "smoke"
    elif args.regression:
        args.markers = "regression"
    
    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    os.makedirs("allure-results", exist_ok=True)
    
    # Run tests
    exit_code = run_tests(args)
    
    # Generate allure report if requested
    if args.allure and exit_code == 0:
        try:
            subprocess.run(["allure", "serve", "allure-results"], check=True)
        except subprocess.CalledProcessError:
            print("Note: Install Allure to view reports: npm install -g allure-commandline")
        except FileNotFoundError:
            print("Note: Allure not found. Install with: npm install -g allure-commandline")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
