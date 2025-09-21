import time
import os
import pytest
from utils.data_reader import read_csv_data
from pages.login_page import LoginPage
from utils.test_result_writer_excel import write_test_results_excel
from datetime import datetime

# Đọc data từ CSV
test_data = read_csv_data("data/login_data.csv")
all_results = []

@pytest.mark.parametrize("index,email,password,expected_result", [
    (i + 1, *row) for i, row in enumerate(test_data)
])
def test_login(browser, index, email, password, expected_result):
    driver = browser
    login_page = LoginPage(driver)

    # Mở trang login
    driver.get("https://thienlong.vn/")
    login_page.open_login_form()
    login_page.login(email, password)

    time.sleep(2)  # đợi cho thông báo hiện

    test_name = f"test_login_{index}"
    screenshot_path = ""
    actual_result = ""
    status = "FAIL"

    try:
        actual_result = login_page.get_error_message(email, password).strip()
        if actual_result == expected_result.strip():
            status = "PASS"
        else:
            raise AssertionError(f"Expected: {expected_result}, Actual: {actual_result}")
    except Exception as e:
        # Lưu screenshot nếu fail
        screenshot_dir = "report/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
        driver.save_screenshot(screenshot_path)
        if not actual_result:
            actual_result = str(e)

    # Lưu kết quả vào all_results
    all_results.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Test Name": test_name,
        "Email": email,
        "Password": password,
        "Expected": expected_result,
        "Actual": actual_result,
        "Status": status,
        "Screenshot": screenshot_path if status == "FAIL" else ""
    })

    # Raise assertion để pytest biết test fail
    assert status == "PASS", f"[{test_name}] Expected: {expected_result}, Actual: {actual_result}"

def teardown_module(module):
    # Ghi kết quả ra Excel sau khi chạy xong tất cả testcase
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report/test_results_login_{timestamp}.xlsx"
    write_test_results_excel(
        all_results,
        filename=filename,
        sheet_name="Test Results Login"
    )