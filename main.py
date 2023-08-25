import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from read_excel import ReadExcel
from twilio_automation import TwilioAutomation
from salesforce import SalesForce

def setup(driver_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(r"--profile-directory=Profile 1")
    chrome_options.add_argument(r"--user-data-dir=C:\\Users\\02009465\\Documents\\Auto Profile")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # service = Service(r'C:\\Users\\02009465\\Documents\\automation\\chromedriver.exe')
    service = Service(driver_path)
    new_driver = webdriver.Chrome(service=service, options=chrome_options)
    return new_driver


###############################################
if __name__ == "__main__":
    driver = setup(r'C:\\Users\\02009465\\Documents\\automation\\chromedriver.exe')

    excel = ReadExcel()
    excel.read_data()

    twilio_automation = TwilioAutomation(excel, driver)

    salesforce = SalesForce(driver, excel)
    salesforce.uatc_login()
    #selenium_automation.upload_image()
    src = salesforce.create_public_link()

    twilio_automation.variable_control()
    twilio_automation.navigate_to_twilio()
    twilio_automation.create_new_template(src)
    twilio_automation.whatsapp_approval()
    time.sleep(10)
    twilio_automation.quit_driver()