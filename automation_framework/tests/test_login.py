import pytest
from automation_framework.pages.login_page import LoginPage
from automation_framework.utils.test_data import get_credentials


@pytest.mark.smoke
def test_login_with_invalid_credentials(browser, base_url):
    login_page = LoginPage(browser)
    login_page.open(base_url)

    username, password = get_credentials("invalid")
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.submit()

    assert "invalid" in login_page.get_error_text().lower()
