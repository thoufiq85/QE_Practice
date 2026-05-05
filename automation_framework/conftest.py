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
    if config.get("headless", False):
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(config.get("implicit_wait", 10))
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def base_url(config):
    return config.get("base_url")
