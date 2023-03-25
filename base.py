from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

TIMEOUT = 10


class BasePage:

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self, url=''):
        self.driver.get(self.base_url + url)

    def set_http_proxy(self, proxy_host, proxy_port, proxy_username=None, proxy_password=None):
        """
        Configures the HTTP proxy for the webdriver.

        Args:
            proxy_host (str): The hostname or IP address of the proxy server.
            proxy_port (int): The port number of the proxy server.
            proxy_username (str, optional): The username to use for authentication with the proxy server.
            proxy_password (str, optional): The password to use for authentication with the proxy server.
        """
        proxy = f"{proxy_host}:{proxy_port}"
        if proxy_username and proxy_password:
            credentials = f"{proxy_username}:{proxy_password}"
            proxy = f"{credentials}@{proxy}"
        self.driver.desired_capabilities['proxy'] = {
            'proxyType': 'manual',
            'httpProxy': proxy,
            'sslProxy': proxy
        }

    def set_socks_proxy(self, proxy_host, proxy_port, proxy_username=None, proxy_password=None):
        """
        Configures the SOCKS proxy for the webdriver.

        Args:
            proxy_host (str): The hostname or IP address of the proxy server.
            proxy_port (int): The port number of the proxy server.
            proxy_username (str, optional): The username to use for authentication with the proxy server.
            proxy_password (str, optional): The password to use for authentication with the proxy server.
        """
        proxy = f"{proxy_host}:{proxy_port}"
        if proxy_username and proxy_password:
            credentials = f"{proxy_username}:{proxy_password}"
            proxy = f"{credentials}@{proxy}"
        self.driver.desired_capabilities['proxy'] = {
            'proxyType': 'manual',
            'socksProxy': proxy,
            'socksVersion': 5
        }

    def set_proxy_autoconfig_url(self, url):
        """
        Configures the automatic proxy configuration URL for the webdriver.

        Args:
            url (str): The URL of the proxy autoconfiguration file.
        """
        self.driver.desired_capabilities['proxy'] = {
            'proxyType': 'pac',
            'pacUrl': url
        }

    def disable_proxy(self):
        """
        Disables the proxy settings for the webdriver.
        """
        self.driver.desired_capabilities['proxy'] = {}

    def find_element(self, locator, condition=EC.presence_of_element_located):
        wait = WebDriverWait(self.driver, TIMEOUT)
        try:
            return wait.until(condition(locator))
        except TimeoutException:
            raise ValueError(f"Element with locator '{locator}' not found")

    def click(self, locator):
        self.find_element(locator).click()

    def send_keys(self, locator, keys):
        self.find_element(locator).send_keys(keys)

    def get_text(self, locator):
        return self.find_element(locator).text

    def is_displayed(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False

    def switch_to_frame(self, locator):
        self.driver.switch_to.frame(self.find_element(locator))

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def get_cookie_value(self, name):
        cookies = self.driver.get_cookies()
        cookie = next((cookie for cookie in cookies if cookie['name'] == name), None)
        return cookie['value'] if cookie else None

    def set_cookie_value(self, name, value):
        self.driver.add_cookie({'name': name, 'value': value})

    def open_new_window(self, url=''):
        self.execute_script(f"window.open('{self.base_url}{url}');")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_window(self):
        self.driver.close()

    def maximize_window(self):
        self.driver.maximize_window()

    def set_window_size(self, width, height):
        self.driver.set_window_size(width, height)

    def set_window_position(self, x, y):
        self.driver.set_window_position(x, y)

    def move_to_element(self, locator):
        ActionChains(self.driver).move_to_element(self.find_element(locator)).perform()

    def get_attribute_value(self, locator, attribute):
        return self.find_element(locator).get_attribute(attribute)

    def execute_script(self, script, *args):
        self.driver.execute_script(script, *args)

    def wait_for_element_to_disappear(self, locator):
        wait = WebDriverWait(self.driver, TIMEOUT)
        try:
            wait.until_not(EC.presence_of_element_located(locator))
        except TimeoutException:
            pass

    def select_dropdown_option_by_text(self, locator, option_text):
        Select(self.find_element(locator)).select_by_visible_text(option_text)

    def get_selected_dropdown_option_text(self, locator):
        return Select(self.find_element(locator)).first_selected_option.text

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
        with self.driver.switch_to.alert as alert:
            alert.accept()

    def dismiss_alert(self):
        with self.driver.switch_to.alert as alert:
            alert.dismiss()

    def get_alert_text(self):
        with self.driver.switch_to.alert as alert:
            return alert.text

    def send_alert_text(self, text):
        with self.driver.switch_to.alert as alert:
            alert.send_keys(text)
            alert.accept()

    def go_back(self):
        self.driver.back()

    def go_forward(self):
        self.driver.forward()
