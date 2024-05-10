import time
from selenium.webdriver.common.by import By
import pyperclip
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller

class SalesForce:
    def __init__(self, driver, excel):
        self.driver = driver
        self.excel = excel

    def uatc_login(self):
        self.driver.get("https://here2serve-cicd.lightning.force.com/lightning/setup/ManageUsers/home")
        time.sleep(2)

        copado_id_input = self.driver.find_element(By.ID, "username")
        copado_id_input.send_keys('example ID') #replace with your ID
        copado_pw_input = self.driver.find_element(By.ID, "password")
        copado_pw_input.send_keys('example password') #replace with your PW

        copado_login_btn = self.driver.find_element(By.ID, "Login")
        copado_login_btn.click()

        time.sleep(3)

        role = "admin1"
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'force-aloha-page')))
        iframe = self.driver.find_element(By.TAG_NAME, 'force-aloha-page').find_element(By.TAG_NAME, 'iframe')
        self.driver.switch_to.frame(iframe)
        time.sleep(5)

        trs = self.driver.find_elements(By.TAG_NAME, "tr")
        trs = trs[2:-1]
        for tr in trs:
            name = tr.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
            if name == role:
                tr.find_elements(By.CSS_SELECTOR, 'td > a')[1].click()

                self.driver.switch_to.default_content()
                time.sleep(5)
                self.driver.switch_to.window(self.driver.window_handles[1])
                # self.driver.close()
                # self.driver.switch_to.window(self.driver.window_handles[0])
                break
        time.sleep(5)

        self.driver.get("https://here2serve-cicd.lightning.force.com/lightning/r/copado__Org__c/a0v5g0000005tqQAAQ/view")
        time.sleep(5)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'force-aloha-page')))
        iframe = self.driver.find_element(By.TAG_NAME, 'force-aloha-page').find_element(By.TAG_NAME, 'iframe')
        self.driver.switch_to.frame(iframe)
        time.sleep(5)

        open_org_btn = self.driver.find_element(By.ID, "thePage:theForm:pb_createOrg:openBtnId")
        open_org_btn.click()
        # self.driver.switch_to.window(self.driver.window_handles[2])
        time.sleep(10)
        # self.driver.close()
        self.driver.get("https://here2serve--uatc.sandbox.lightning.force.com/lightning/o/ContentDocument/home")
        self.driver.switch_to.window(self.driver.window_handles[1])

        time.sleep(10)


    def upload_image(self):
        upload_file_btn_div = self.driver.find_element(By.XPATH,"/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[2]/section[1]/div/div/section/div/div[2]/div/div/div/div[1]/div/div[2]/ul/li/a")
        time.sleep(1)
        upload_file_btn = upload_file_btn_div.find_element(By.XPATH,'//*[@id="brandBand_2"]/div/div/div[1]/div/div[2]/ul/li/a')
        upload_file_btn_div.click()
        time.sleep(3)

        keyboard = Controller()

        keyboard.type("C:\\Users\\02009465\\Documents\\automation\\media\\image2.png")
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        time.sleep(5)
        # keyboard.press(Key.enter)
        # keyboard.release(Key.enter)/html/body/div[4]/div[2]/div/div[2]/div/div[3]/div/span[2]/button
        done_btn = self.driver.find_element(By.XPATH,
                                            "/html/body/div[4]/div[2]/div/div[2]/div/div[3]/div/span[2]/button")
        done_btn.click()

        # upload_file_btn.send_keys("C:\\Users\\02009465\\Documents\\automation\\image2.png")
        time.sleep(5)

    def create_public_link(self):
        table = self.driver.find_element(By.XPATH,
                                         "/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[2]/section[1]/div/div/section/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div/table/tbody")
        rows = table.find_elements(By.XPATH, "*")
        for i in rows:
            if self.excel.img_name in i.text:
                triangle = i.find_element(By.XPATH, "./td[4]/span/div")
                triangle.click()
        time.sleep(2)

        public_link_btn = self.driver.find_element(By.XPATH, "/html/body/div[8]/div/ul/li[3]/a")
        public_link_btn.click()
        time.sleep(3)

        try:  # when expiration date is checked
            self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[2]")
            expire_date_turnoff = self.driver.find_element(By.XPATH,
                                                           "/html/body/div[4]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/lightning-input/div/label/span[2]/span[1]")
            expire_date_turnoff.click()
            time.sleep(2)
            create_link_btn = self.driver.find_element(By.XPATH,
                                                       "/html/body/div[4]/div[2]/div/div[2]/div/div[2]/div/div/div[4]/div[2]/div/div[1]/button")
            create_link_btn.click()
            time.sleep(2)

            create_btn = self.driver.find_element(By.XPATH,
                                                  "/html/body/div[4]/div[2]/div[2]/div[2]/div/div[3]/button[2]/span")
            create_btn.click()
            time.sleep(2)
        except:  # when expieration date is unchecked
            pass

        copy_link_btn = self.driver.find_element(By.XPATH,
                                                 "/html/body/div[4]/div[2]/div/div[2]/div/div[2]/div/div/div[4]/div[2]/div/div[1]/div/button")
        copy_link_btn.click()
        time.sleep(2)
        # actions.send_keys(Keys.ESCAPE)
        time.sleep(3)
        image_url = pyperclip.paste()
        print(image_url)

        self.driver.get(image_url)
        time.sleep(8)
        image = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[4]/div/img')
        src = image.get_attribute('src')

        return src
