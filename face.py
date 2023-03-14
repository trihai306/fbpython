from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from base import TIMEOUT, BasePage


class FacebookPage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        # Khai báo các phần tử trên trang đăng nhập
        self.email_input = (By.ID, 'm_login_email')
        self.password_input = (By.ID, 'm_login_password')
        self.login_button = (By.NAME, 'login')
        self.LIKE_BUTTON_LOCATOR = (By.XPATH, "//span[text()='Like']")
        self.LIKE_STATUS_LOCATOR = (By.XPATH, "//div[contains(@class,'_666k') and contains(@class,'_8o')]/a/span[1]")
        self.SHARE_BUTTON_LOCATOR = (By.XPATH, "//span[text()='Share']")
        self.WRITE_POST_INPUT_LOCATOR = (By.XPATH, "//textarea[contains(@name,'mercur')]")
        self.POST_BUTTON_LOCATOR = (By.XPATH, "//button[contains(.,'Post')]")
        self.COMMENT_INPUT_LOCATOR = (By.XPATH, "//textarea[contains(@name,'comment_text')]")
        self.COMMENT_BUTTON_LOCATOR = (By.XPATH, "//button[contains(.,'Comment')]")
        self.MESSAGE_BUTTON_LOCATOR = (By.XPATH, "//a[@aria-label='Messenger']")
        self.NEW_MESSAGE_BUTTON_LOCATOR = (By.XPATH, "//div[text()='New Message']")
        self.SEARCH_INPUT_LOCATOR = (By.XPATH, "//input[contains(@placeholder,'Search for people and groups')]")
        self.USER_LIST_LOCATOR = (By.XPATH, "//div[@role='listbox']/ul/li[1]/a")
        self.MESSAGE_INPUT_LOCATOR = (By.XPATH, "//div[contains(@class,'_5rp7')]//div[@contenteditable='true']")
        self.SEND_BUTTON_LOCATOR = (By.XPATH, "//span[text()='Send']")

    def login(self, email, password):
        # Mở trang đăng nhập
        self.open('/login')

        # Nhập thông tin đăng nhập
        self.send_keys(self.email_input, email)
        self.send_keys(self.password_input, password)

        # Nhấn nút đăng nhập
        self.click(self.login_button)

        # Đợi cho trang tải xong
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Welcome")]'))
        )

        # Lưu cookie vào file
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'c_user':
                user_id = cookie['value']
            if cookie['name'] == 'xs':
                xs_token = cookie['value']
        with open('cookies.txt', 'a') as f:
            f.write(f'{email}|{password}|{user_id}|{xs_token}\n')

    def like_post(self):
        self.click(self.LIKE_BUTTON_LOCATOR)
        like_status_before = self.get_text(self.LIKE_STATUS_LOCATOR)
        self.click(self.LIKE_BUTTON_LOCATOR)
        like_status_after = self.get_text(self.LIKE_STATUS_LOCATOR)
        return like_status_before != like_status_after

    def share_post(self, post_content):
        # Click vào nút Share
        self.click(self.SHARE_BUTTON_LOCATOR)

        # Nhập nội dung bài viết
        write_post_input = self.find_element(self.WRITE_POST_INPUT_LOCATOR)
        write_post_input.send_keys(post_content)

        # Chọn mục Share
        self.driver.execute_script("arguments[0].click();",
                                   self.find_element((By.XPATH, "//span[text()='Share Now (Public)']")))

        # Nhấn nút Post để đăng bài viết
        self.click(self.POST_BUTTON_LOCATOR)

    def comment_post(self, comment_content):
        # Nhập nội dung bình luận vào ô textarea
        self.send_keys(self.COMMENT_INPUT_LOCATOR, comment_content)

        # Click vào nút Comment để đăng bình luận
        self.click(self.COMMENT_BUTTON_LOCATOR)

    def send_message(self, user_name, message):
        # Click vào nút Messenger
        self.click(self.MESSAGE_BUTTON_LOCATOR)

        # Click vào nút New Message
        self.click(self.NEW_MESSAGE_BUTTON_LOCATOR)

        # Nhập tên người dùng cần gửi tin nhắn
        self.send_keys(self.SEARCH_INPUT_LOCATOR, user_name)
        self.click(self.USER_LIST_LOCATOR)

        # Nhập nội dung tin nhắn
        self.driver.find_element(*self.MESSAGE_INPUT_LOCATOR).click()
        actions = ActionChains(self.driver)
        actions.send_keys(message)
        actions.perform()


# Sử dụng hàm login để đăng nhập vào trang web
driver = webdriver.Chrome()
facebook_page = FacebookPage(driver, 'https://m.facebook.com/')
facebook_page.login('example@example.com', 'password')
