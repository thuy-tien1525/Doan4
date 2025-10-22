from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class FixPage:
    def __init__(self, driver):
        self.driver = driver
        self.quick_view = (By.XPATH, "//a[@data-handle='tui-but-bi-but-gel-thien-long-luck-phien-ban-hanh-thong-thi-cu']")
        self.btn_add = (By.XPATH, "//button[contains(@class,'btn-addtocart') or contains(text(),'Thêm vào giỏ hàng')]")
        self.product_name = (By.XPATH, "//a[@class='text2line']")
        self.cart_icon = (By.XPATH, "//a[@title='Giỏ hàng']")

        self.text_active = (By.XPATH, "//li[contains(@class,'active') or contains(text(),'Giỏ hàng')]")

    def click_quick_view(self):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.quick_view))
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
            self.driver.execute_script("arguments[0].click();", btn)
            print("Đã click nút 'Thêm vào giỏ hàng' thành công bằng XPath + JS.")
            time.sleep(2)
        except Exception as e:
            print(f"Không click được nút thêm giỏ hàng: {e}")
            raise

    def open_cart(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.cart_icon)).click()
        print(" Đã mở trang giỏ hàng.")
        time.sleep(2)

    def increase_quantity(self):
        try:
            qty_input = self.driver.find_element(By.CSS_SELECTOR, "input.number-sidebar")
            old_val = qty_input.get_attribute("value")

            btn_plus_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'btn-plus')]/i[contains(@class,'fa-plus')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_plus_icon)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", btn_plus_icon)

            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(By.CSS_SELECTOR, "input.number-sidebar").get_attribute("value") != old_val
            )
            new_val = self.driver.find_element(By.CSS_SELECTOR, "input.number-sidebar").get_attribute("value")
            print(f"Số lượng tăng từ {old_val} → {new_val}")
        except Exception as e:
            print(f"Không tăng được số lượng: {e}")

    def decrease_quantity(self):
        try:
            qty_input = self.driver.find_element(By.CSS_SELECTOR, "input.number-sidebar")
            old_val = qty_input.get_attribute("value")

            btn_minus_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'btn-minus')]/i[contains(@class,'fa-minus')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_minus_icon)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", btn_minus_icon)

            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(By.CSS_SELECTOR, "input.number-sidebar").get_attribute("value") != old_val
            )
            new_val = self.driver.find_element(By.CSS_SELECTOR, "input.number-sidebar").get_attribute("value")
            print(f"Số lượng giảm từ {old_val} → {new_val}")
        except Exception as e:
            print(f"Không giảm được số lượng: {e}")

    def remove_product(self, product_name):
        try:
            btn_remove = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     f"//a[contains(text(),'{product_name}')]/ancestor::tr//button[contains(@class,'remove')]")
                )
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_remove)
            time.sleep(5)
            btn_remove.click()
            time.sleep(10)

            print(f"Sản phẩm '{product_name}' đã được xóa thành công!")
        except TimeoutException:
            print(f"Không tìm thấy sản phẩm '{product_name}' trong giỏ → đã xóa thành công.")
        except Exception as e:
            print(f"Lỗi khi xóa sản phẩm: {e}")
            raise

    def get_cart_quantity_and_total(self):
        try:
            qty_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.number-sidebar"))
            )
            total_price_el = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.totals_price_mobile"))
            )

            qty = int(qty_input.get_attribute("value").strip())
            total = total_price_el.text.strip()
            print(f"Số lượng: {qty}, Tổng tiền: {total}")
            return qty, total
        except Exception as e:
            print(f"Không lấy được số lượng hoặc tổng tiền: {e}")
            raise

    def is_cart_page_active(self):
        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.text_active)
            )
            text = el.text.strip()
            print(f" Breadcrumb hiện tại: {text}")
            return "Giỏ hàng" in text
        except TimeoutException:
            print(" Không tìm thấy breadcrumb 'Giỏ hàng'.")
            return False
