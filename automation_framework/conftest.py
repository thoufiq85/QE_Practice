import os
import yaml
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as cfg:
        return yaml.safe_load(cfg)


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture(scope="function")
def browser(config):
    options = ChromeOptions()

    # Force headless mode in CI environments
    is_ci = os.getenv("CI", "false").lower() == "true"
    is_headless = config.get("headless", False) or is_ci

    if is_headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        # Additional arguments for CI environments
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")

    # Common Chrome options for stability
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(config.get("implicit_wait", 10))
        yield driver
    except Exception as e:
        print(f"Failed to create Chrome driver: {e}")
        # Try with basic options if advanced options fail
        options = ChromeOptions()
        if is_headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(config.get("implicit_wait", 10))
        yield driver
    finally:
        driver.quit()


@pytest.fixture(scope="function")
def base_url(config):
    return config.get("base_url")
