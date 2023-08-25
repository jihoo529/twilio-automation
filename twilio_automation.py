import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
from selenium.webdriver import ActionChains
import re

class TwilioAutomation:
    def __init__(self, excel, driver):
        self.excel = excel
        self.driver = driver
        self.action = ActionChains(driver)

    def scroll_down(self):
        self.action.key_down(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        self.action.key_up(Keys.PAGE_DOWN).perform()
        time.sleep(1)
    def variable_control(self):
        text = self.excel.temp_body

        pattern = r"\{\{([^}]+)\}\}"
        matches = re.findall(pattern, text)

        self.body_text = re.sub(pattern, lambda m: f"{{{{{matches.index(m.group(1)) + 1}}}}}", text)

        self.dict_variables = {i + 1: match for i, match in enumerate(matches)}

        self.url_variable = len(matches) + 1

    def navigate_to_twilio(self):
        time.sleep(3)
        self.driver.get("https://console.twilio.com/?frameUrl=%2Fconsole%3Fx-target-region%3Dus1")
        self.driver.implicitly_wait(10)

        try:
            email_input = self.driver.find_element(By.ID, "email")
            email_input.send_keys("jihoo.lee@pccw.com")
            continue_btn = self.driver.find_element(By.ID, "email-next")
            continue_btn.click()
            time.sleep(3)

            pw_input = self.driver.find_element(By.ID, "password")
            pw_input.send_keys("Key@exlogin727472")

            login_btn = self.driver.find_element(By.ID, "login")
            login_btn.click()
            time.sleep(3)
        except:
            pass

    ################ Create New Template ###################
    def create_new_template(self, src):
        pattern = r"(?<=version/)(.*)"
        match = re.search(pattern, src)
        self.url_suffix = match.group(1)
        self.replaced_url = re.sub(pattern, f"{{{{{self.url_variable}}}}}", src)

        btn_messaging = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div[1]/div[1]/div/div/div/span[2]')
        btn_messaging.click()
        time.sleep(2)

        btn_content_editor = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[2]/div[5]/div[1]/a/div')
        btn_content_editor.click()
        time.sleep(2)

        btn_create_new = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[1]/div[2]/div/button')
        btn_create_new.click()
        time.sleep(2)

        temp_name_input = self.driver.find_element(By.ID, "create_page_name")
        temp_name_input.send_keys(self.excel.temp_name)
        time.sleep(2)

        temp_lang_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div/div[1]/article/div/div[1]/div[2]/div/div/div[1]/div/input")
        temp_lang_input.send_keys(self.excel.temp_lang)
        time.sleep(2)

        container = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[3]/div/div/div[1]/article/div/div[2]/div[1]/fieldset/div/div/div')
        print("###", container)
        # access child elements of container
        time.sleep(2)
        boxes = container.find_elements(By.XPATH, '*')

        idx = 0
        self.scroll_down()

        for b in boxes:
            b_text = b.get_attribute('textContent')
            if self.excel.temp_type in b_text:
                print(f'idx = {idx}')
                print(b)
                b.click()
                # btn = b.find_element(By.XPATH, './/label//div')
                # btn.click()
            idx += 1

        time.sleep(2)

        btn_create_temp = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div/div[2]/div[2]/div/div[1]/button")
        btn_create_temp.click()
        time.sleep(5)

        ################### input body text ############################
        temp_body_input = self.driver.find_element(By.ID, "title")
        pyperclip.copy(self.body_text)
        temp_body_input.send_keys(Keys.CONTROL, 'v')

        footer_input = self.driver.find_element(By.ID, "card-subtitle")
        footer_input.send_keys(self.excel.temp_footer)

        url_input = self.driver.find_element(By.ID, "media-url")
        url_input.send_keys(self.replaced_url)

        self.scroll_down()

        # can't click here
        btn_type = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div/div/div[2]/div[2]/article/div/div/div[1]/div/div/div/div[3]/div/div[1]/div")
        btn_type.click()
        time.sleep(2)
        print(self.excel.btn_type)
        container = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div/div/div[2]/div[2]/article/div/div/div[1]/div/div/div/div[3]/div/div[2]")
        lists = container.find_element(By.XPATH, "./*")

        quick_reply = lists.find_element(By.XPATH, "./li[2]")
        call_to_action = lists.find_element(By.XPATH, "./li[3]")

        self.scroll_down()

        if self.excel.btn_type == "Quick Reply":
            quick_reply.click()
            time.sleep(1)
            self.quick_reply()
        else:
            call_to_action.click()
            time.sleep(1)
            self.call_to_action()

    def call_to_action(self):
        self.scroll_down()

        opts = self.excel.call_to_action_opts

        type_of_action = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div/div/div[2]/div[2]/article/div/div/div[1]/div/div/div/div[4]/div/article/div[2]/div[1]/div/div[1]/div")
        type_of_action.click()
        time.sleep(2)

        container = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div/div/div[2]/div[2]/article/div/div/div[1]/div/div/div/div[4]/div/article/div[2]/div[1]/div/div[2]")
        time.sleep(1)
        lists = container.find_element(By.XPATH, "*")
        time.sleep(1)

        phone_number = lists.find_element(By.XPATH, "./li[2]")
        view_website = lists.find_element(By.XPATH, "./li[3]")

        if opts['Type of action'].lower() == 'website':
            view_website.click()
            action_type = 'button'
        else:
            phone_number.click()
            action_type = 'phone'

        btn_text = self.driver.find_element(By.ID, "cta-button-text-0")
        btn_text.send_keys(opts['Button text'])
        time.sleep(1)

        phone_number = self.driver.find_element(By.ID, f"cta-{action_type}-value-0")
        phone_number.send_keys(opts['Website URL'])
        time.sleep(2)

    def quick_reply(self):
        self.scroll_down()
        quick_reply_opts = self.excel.quick_reply_opts

        for i in quick_reply_opts:
            btn_id = f'qr-button-text-{i}'
            button_text_input = self.driver.find_element(By.ID, btn_id)
            button_text_input.send_keys(quick_reply_opts[i])
            time.sleep(2)

            if i < len(quick_reply_opts) - 1:
                add_button_container = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[3]/div/div/div/div[2]/div[2]/article/div/div/div[1]/div/div/div/div[5]')
                time.sleep(1)
                add_btn = add_button_container.find_element(By.XPATH, '*')
                add_btn.click()
                time.sleep(2)

            self.scroll_down()

        print(quick_reply_opts)

    def whatsapp_approval(self):
        btn_whatsapp_approval = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div/div/div[3]/div[2]/div/div/div/div[2]/button")
        btn_whatsapp_approval.click()
        time.sleep(2)

        container = self.driver.find_element(By.XPATH, "/html/body/reach-portal/div[2]/div/div/div/div[2]/div/div/div")
        time.sleep(1)
        # container_child = container.find_element(By.XPATH, "./div/div")
        num_container_child = len(container.find_elements(By.XPATH, "*"))

        media_url_div = container.find_element(By.XPATH, "./div[1]")
        media_url_div.click()

        media_url_input = media_url_div.find_element(By.XPATH, "./article/div/div/div/div/input")
        media_url_input.send_keys(self.url_suffix)

        if num_container_child > 1:
            title_div = container.find_element(By.XPATH, "./div[2]")
            title_div.click()
            time.sleep(1)

            title_container = self.driver.find_element(By.XPATH,"/html/body/reach-portal/div[2]/div/div/div/div[2]/div/div/div/div[2]/article/div")

            for i in self.dict_variables:
                title_input = title_container.find_element(By.XPATH, f"./div[{i}]/div/div/input")
                title_input.send_keys(self.dict_variables[i])

                self.scroll_down()

        save_btn = self.driver.find_element(By.XPATH, "/html/body/reach-portal/div[2]/div/div/div/div[3]/div[2]/div/div/div/button")
        save_btn.click()
        time.sleep(1)

        categories = self.driver.find_element(By.XPATH, "/html/body/reach-portal/div[2]/div/div/div/div[2]/fieldset/div/div[2]")

        if self.excel.temp_category == 'Marketing':
            div = categories.find_element(By.XPATH, "./div[1]")
        else:
            div = categories.find_element(By.XPATH, "./div[2]")
        div.find_element(By.XPATH, "./label").click()
        time.sleep(2)

        submit_btn = self.driver.find_element(By.XPATH, "/html/body/reach-portal/div[2]/div/div/div/div[3]/div/div/div/div[2]/button")
        submit_btn.click()

    def quit_driver(self):
        self.driver.quit()