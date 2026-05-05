#!/usr/bin/env python3
"""
Simple test script to debug local pytest issues
"""
import os
import sys
import time

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from automation_framework.conftest import load_config
    from automation_framework.utils.test_data import get_credentials
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from webdriver_manager.chrome import ChromeDriverManager

    print("✓ All imports successful")

    # Test config loading
    config = load_config()
    print(f"✓ Config loaded: {config}")

    # Test CI detection
    is_ci = os.getenv("CI", "false").lower() == "true"
    is_headless = config.get("headless", False) or is_ci
    print(f"✓ CI detection: CI={is_ci}, Headless={is_headless}")

    # Test credentials
    username, password = get_credentials("invalid")
    print(f"✓ Credentials loaded: {username}, {password}")

    # Test Chrome setup
    print("Setting up Chrome...")
    options = ChromeOptions()
    if is_headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        print("Running in headless mode")
    else:
        print("Running in normal mode (windowed)")

    options.add_argument("--window-size=1920,1080")

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        print("✓ Chrome driver created successfully")

        driver.get("https://www.google.com")
        print("✓ Successfully navigated to Google")

        driver.quit()
        print("✓ Chrome driver closed successfully")

    except Exception as e:
        print(f"✗ Chrome setup failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed! The framework should work locally.")

except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)</content>
<parameter name="filePath">c:\Users\Mohammed Thoufiq\Desktop\Resume\RBC\QE\P\QE_Practice\test_local_setup.py