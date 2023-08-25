from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains

service = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = "https://here2serve-cicd.lightning.force.com/lightning/setup/ManageUsers/home"
url2 = "https://here2serve-cicd.lightning.force.com/lightning/_classic/%2Fa11%2Fo"
driver.get(url)

username_box_xpath = "/html/body/div[1]/div[1]/div/div/div[2]/div[3]/form/div[2]/div/input[1]"
password_box_xpath = "/html/body/div[1]/div[1]/div/div/div[2]/div[3]/form/input[2]"

username_input = driver.find_element(By.XPATH, username_box_xpath)
password_input = driver.find_element(By.XPATH, password_box_xpath)

username_input.send_keys("jihoo.lee@pccw.com.copado")
password_input.send_keys("key@exlogin01")
password_input.send_keys(Keys.ENTER)
time.sleep(20)
# Close the driver after 30 seconds



element_xpath = '//*[@id="ResetForm"]/div[2]/table/tbody/tr[5]/td[1]/a[2]'
elements = driver.find_elements(By.XPATH, element_xpath)
for element in elements:
    element.click()

time.sleep(60)
driver.quit()