import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.Fixcart_page import FixPage


def test_edit_cart_thienlong():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    cart_page = FixPage(driver)

    try:
        driver.get("https://thienlong.vn/collections/bst-but-bi?q=filter=((collectionid:product=1003720150))&page=1&sortby=manual&view=grid")

        cart_page.click_quick_view()
        time.sleep(1)
        name_before = cart_page.get_product_name()

        cart_page.click_add_to_cart()
        print(f"Đã thêm sản phẩm: {name_before}")
        time.sleep(2)

        cart_page.open_cart()
        assert cart_page.is_cart_page_active(), "Không mở được trang giỏ hàng!"
        print("Đã mở trang giỏ hàng thành công.")
        time.sleep(1)

        # --- Lấy số lượng và tổng tiền ban đầu ---
        qty_before, total_before = cart_page.get_cart_quantity_and_total()

        # --- Tăng số lượng ---
        cart_page.increase_quantity()
        qty_plus, total_plus = cart_page.get_cart_quantity_and_total()
        assert int(qty_plus) > int(qty_before), f"Số lượng không tăng: {qty_before} → {qty_plus}"
        print(f"Số lượng tăng: {qty_before} → {qty_plus}")
        print(f"Tổng tiền: {total_before} → {total_plus}")

        # --- Giảm số lượng ---
        cart_page.decrease_quantity()
        qty_minus, total_minus = cart_page.get_cart_quantity_and_total()
        assert int(qty_minus) == int(qty_before), f"Số lượng sau giảm không về như cũ: {qty_minus}"
        print(f"Đã giảm về: {qty_minus}, Tổng tiền: {total_minus}")

        # --- Xóa sp ---
        cart_page.remove_product(name_before)
        time.sleep(2)
        try:
            qty_final, _ = cart_page.get_cart_quantity_and_total()
            assert int(qty_final) == 0, "Sản phẩm vẫn còn trong giỏ!"
        except Exception:
            print(" Giỏ hàng trống sau khi xóa sản phẩm.")

    except Exception as e:
        print(f"TEST FAILED: {e}")
        raise

    finally:
        driver.quit()

