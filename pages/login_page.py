from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.open_login_btn = (By.XPATH, "//a[@class='font-weight-bold']")
        self.email_input = (By.ID, "customer_email")
        self.password_input = (By.ID, "customer_password")
        self.login_btn = (By.XPATH, "//button[contains(text(),'Đăng nhập')]")
        self.error_msg_toast = (By.CSS_SELECTOR, ".toast-message")
        self.error_msg_static = (By.XPATH, "//div[@class='form-signup margin-bottom-15']")
        self.greeting_text = (By.XPATH, "(//a[contains(text(),'Hi, Phạm Tiên')])[1]")


    def open(self, url):
        self.driver.get(url)
    def open_login_form(self):
        self.driver.find_element(*self.open_login_btn).click()

    def login(self, email, password):
        self.driver.find_element(*self.email_input).clear()
        self.driver.find_element(*self.email_input).send_keys(email or "")
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password or "")
        self.driver.find_element(*self.login_btn).click()

    def get_error_message(self, email, password, timeout=3):


        if not email or "@" not in email or ".." in email or email.endswith("@") or "@@" in email:
            return self.driver.find_element(*self.email_input).get_attribute("validationMessage")
        if not password:
            return self.driver.find_element(*self.password_input).get_attribute("validationMessage")

        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text.strip()
            alert.accept()
            return text
        except TimeoutException:
            pass

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.error_msg_toast)
            )
            return element.text.strip()
        except TimeoutException:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(self.error_msg_static)
                )
                return element.text.strip()
            except TimeoutException:
                pass

        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.greeting_text)
            )
            return element.text.strip()
        except TimeoutException:
            return "Không tìm thấy thông báo"
