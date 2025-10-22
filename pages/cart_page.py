from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.quick_view = (By.XPATH, "//a[@data-handle='tui-but-bi-but-gel-thien-long-luck-phien-ban-hanh-thong-thi-cu']")
        self.btn_add = (By.CSS_SELECTOR, "btn_cool btn btn_base fix_add_to_cart ajax_addtocart btn_add_cart btn-cart add_to_cart add_to_cart_detail")
        self.cart_icon = (By.XPATH, "//a[@title='Giỏ hàng']")
        self.text_cart = (By.XPATH, "//a[@class='text2line']")
        self.product_name = (By.XPATH, "//a[@class='text2line']")

        self.btn_minus = (By.CSS_SELECTOR, "reduced items-count btn-minus btn")
        self.btn_plus = (By.CSS_SELECTOR, "increase items-count btn-plus btn")
        self.btn_remove = (By.CSS_SELECTOR, "remove-itemx remove-item-cart")
        self.input_number = (By.CSS_SELECTOR, "form-control input-text number-sidebar qtyMobile1151929586")
        self.total_price = (By.CSS_SELECTOR, "text-xs-right  totals_price_mobile")
        self.text_active = (By.XPATH, "//li[@class='active']")

    def click_quick_view(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.quick_view)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

    def get_product_name(self):
        try:
            name = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.product_name)
            ).text
            print(f"Tên sản phẩm trước khi thêm: {name}")
            return name
        except TimeoutException:
            raise Exception("Không tìm thấy tên sản phẩm!")

    def click_add_to_cart(self):
        try:
            btn = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//body[1]/div[3]/div[2]/div[1]/div[1]/div[2]/form[1]/div[5]/div[1]/div[2]/button[1]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(1)

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//body[1]/div[3]/div[2]/div[1]/div[1]/div[2]/form[1]/div[5]/div[1]/div[2]/button[1]"))
            )
            self.driver.execute_script("arguments[0].click();", btn)
            print("Đã click nút 'Thêm vào giỏ hàng' thành công bằng XPath + JS.")
            time.sleep(3)

        except Exception as e:
            print(f"Không click được nút thêm giỏ hàng: {e}")
            print("HTML snippet quanh nút:", btn.get_attribute("outerHTML") if 'btn' in locals() else "Không thấy nút")
            raise

    def open_cart(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.cart_icon)
        ).click()
    def get_text_in_cart(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.text_cart)
            )
            name_in_cart = element.text.strip()
            print(f"Sản phẩm trong giỏ: {name_in_cart}")
            return name_in_cart
        except TimeoutException:
            raise Exception("Không tìm thấy tên sản phẩm trong giỏ hàng!")


