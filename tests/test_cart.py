from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pages.cart_page import CartPage
import time

def test_add_to_cart_thienlong():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get("https://thienlong.vn/collections/bst-but-bi?q=filter=((collectionid:product=1003720150))&page=1&sortby=manual&view=grid")

    cart_page = CartPage(driver)

    cart_page.click_quick_view()
    time.sleep(2)

    name_before = cart_page.get_product_name()
    print(f"Sản phẩm được chọn: {name_before}")

    cart_page.click_add_to_cart()
    time.sleep(3)

    cart_page.open_cart()
    time.sleep(3)

    name_in_cart = cart_page.get_text_in_cart()
    print(f"Sản phẩm trong giỏ: {name_in_cart}")

    assert name_before.strip().lower() in name_in_cart.strip().lower(), \
        f"Expected {name_before}, but got {name_in_cart}"
    print(f"PASSED: {name_before} xuất hiện trong giỏ hàng")

    driver.quit()
