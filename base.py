from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

TIMEOUT = 10


class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self, url=''):
        self.driver.get(self.base_url + url)

    def find_element(self, locator, timeout=TIMEOUT, condition=EC.presence_of_element_located):
        try:
            return WebDriverWait(self.driver, timeout).until(condition(locator))
        except TimeoutException:
            raise ValueError(f"Element with locator '{locator}' not found")

    def click(self, locator, timeout=TIMEOUT):
        self.find_element(locator, timeout).click()

    def send_keys(self, locator, keys, timeout=TIMEOUT):
        self.find_element(locator, timeout).send_keys(keys)

    def get_text(self, locator, timeout=TIMEOUT):
        return self.find_element(locator, timeout).text

    def is_displayed(self, locator, timeout=TIMEOUT):
        try:
            return self.find_element(locator, timeout).is_displayed()
        except:
            return False

    def switch_to_frame(self, locator, timeout=TIMEOUT):
        self.driver.switch_to.frame(self.find_element(locator, timeout))

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def get_cookie_value(self, name):
        cookies = self.driver.get_cookies()
        cookie = next((cookie for cookie in cookies if cookie['name'] == name), None)
        return cookie['value'] if cookie else None

    def set_cookie_value(self, name, value):
        self.driver.add_cookie({'name': name, 'value': value})

    def open_new_window(self, url=''):
        self.execute_script("window.open('" + self.base_url + url + "');")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_window(self):
        self.driver.close()

    def maximize_window(self):
        self.driver.maximize_window()

    def set_window_size(self, width, height):
        self.driver.set_window_size(width, height)

    def set_window_position(self, x, y):
        self.driver.set_window_position(x, y)

    def move_to_element(self, locator, timeout=TIMEOUT):
        ActionChains(self.driver).move_to_element(self.find_element(locator, timeout)).perform()

    def get_attribute_value(self, locator, attribute, timeout=TIMEOUT):
        return self.find_element(locator, timeout).get_attribute(attribute)

    def execute_script(self, script, *args):
        self.driver.execute_script(script, *args)

    def wait_for_element_to_disappear(self, locator, timeout=TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            pass

    def select_dropdown_option_by_text(self, locator, option_text, timeout=TIMEOUT):
        Select(self.find_element(locator, timeout)).select_by_visible_text(option_text)

    def get_selected_dropdown_option_text(self, locator, timeout=TIMEOUT):
        return Select(self.find_element(locator, timeout)).first_selected_option.text

    def press_key(self, key):
        ActionChains(self.driver).send_keys(key).perform()

    def press_enter_key(self):
        self.press_key(Keys.ENTER)

    def press_tab_key(self):
        self.press_key(Keys.TAB)

    def save_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    def get_page_title(self):
        return self.driver.title

    def accept_alert(self):
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        self.driver.switch_to.alert.dismiss()

    def get_alert_text(self):
        return self.driver.switch_to.alert.text

    def send_alert_text(self, text):
        alert = self.driver.switch_to.alert
        alert.send_keys(text)
        alert.accept()

    def go_back(self):
        self.driver.back()

    def go_forward(self):
        self.driver.forward()
