from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "submit")
        self.error_message = (By.ID, "error")

    def open(self, base_url: str):
        self.driver.get(base_url)

    def enter_username(self, username: str):
        self.driver.find_element(*self.username_input).clear()
        self.driver.find_element(*self.username_input).send_keys(username)

    def enter_password(self, password: str):
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)

    def submit(self):
        self.driver.find_element(*self.login_button).click()

    def get_error_text(self) -> str:
        return self.driver.find_element(*self.error_message).text
