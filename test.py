import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.select import Select
import pandas as pd
import pyperclip
from selenium.webdriver import ActionChains

class TwilioAutomation:
    def __init__(self):
        self.col_names = ['Template name', 'Message Content', 'Three Quick button reply', 'Category ', 'Language', 'Account SID']
        self.sheet_name = 'i_mob_retail_FlipFold1010_pic'
        self.file_path = r'C:\Users\02009465\Documents\automation\test_csv.xlsx'
    
    def read_data(self):
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)

        json_str = df.to_json(orient='records')

        self.template = df.to_dict()
        
        self.temp_name = self.template['Template name'][0].lower()
        self.temp_body = self.template['Message Content'][0]
        self.temp_lang = self.template['Language'][0]
        self.temp_type = 'Quick reply'
        self.quick_reply_opts = self.template['Three Quick button reply']

        for idx,value in self.template['Message Content'].items():
            if pd.isna(value):
                continue
            #print(value)

###############################################

class SeleniumAutomation:
    def __init__(self, twilio):
        self.twilio = twilio

    def setup(self, driver_path):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(r"--profile-directory=Profile 1")
        chrome_options.add_argument(r"--user-data-dir=C:\\Users\\02009465\\Documents\\Auto Profile")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        #service = Service(r'C:\\Users\\02009465\\Documents\\automation\\chromedriver.exe')
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

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
    def create_new_template(self):
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
        temp_name_input.send_keys(self.twilio.temp_name)
        time.sleep(2)

        temp_lang_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div/div[1]/article/div/div[1]/div[2]/div/div/div[1]/div/input")
        temp_lang_input.send_keys(self.twilio.temp_lang)
        time.sleep(3)

        #container = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[3]/div/div/div[1]/article/div/div[2]/div[1]/fieldset/div/div')
        container = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[3]/div/div/div[1]/article/div/div[2]/div[1]/fieldset/div/div/div')
        #access child elements of container
        time.sleep(3)
        boxes = container.find_elements(By.XPATH, '*')

        idx = 0
        for b in boxes:
            b_text = b.get_attribute('textContent')
            if twilio.temp_type in b_text:
                print(f'idx = {idx}')
                b.click()
            time.sleep(1)
        time.sleep(2)

        btn_create_temp = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div/div[2]/div[2]/div/div[1]/button")
        btn_create_temp.click()
        time.sleep(5)


        temp_body_input = self.driver.find_element(By.ID, "body")
        pyperclip.copy(self.twilio.temp_body)
        temp_body_input.send_keys(Keys.CONTROL, 'v')
        
        '''
        act = ActionChains(self.driver)
        act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        #temp_body_input.send_keys(self.twilio.temp_body)
        '''
        time.sleep(2)

        opts_list = self.twilio.quick_reply_opts

        num_opts = len(opts_list)
        for i in opts_list:
            btn_id = f'qr-button-text-{i}'
            button_text_input = self.driver.find_element(By.ID, btn_id)
            button_text_input.send_keys(opts_list[i])
            time.sleep(2)

            if i < len(opts_list)-1:
                add_button_container = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[3]/div/div/div/div[2]/div[2]/article/div/div/div[1]/div/div/div[5]')
                time.sleep(1)
                add_btn = add_button_container.find_element(By.XPATH, '*')
                add_btn.click()
                time.sleep(2)

        print(opts_list)


    def quit_driver(self):
        self.driver.quit()

if __name__ == "__main__":
    twilio = TwilioAutomation()
    twilio.read_data()

    selenium_automation = SeleniumAutomation(twilio)
    selenium_automation.setup(r'C:\\Users\\02009465\\Documents\\automation\\chromedriver.exe')
    selenium_automation.navigate_to_twilio()
    selenium_automation.create_new_template()
    selenium_automation.quit_driver()