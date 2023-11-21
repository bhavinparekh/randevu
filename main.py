import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib

chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
prefs = {"plugins.always_open_pdf_externally": False}
chrome_options.add_experimental_option("prefs", prefs)

sender_email = "--write--"
rec_email = "--write--"
password = "--write--"
msg = ""

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, password)
print("l success")

import sched, time

s = sched.scheduler(time.time, time.sleep)


def do_something(sc):
    with webdriver.Chrome(executable_path="chromedriver", options=chrome_options) as driver:
        driver.get('https://www.seine-saint-denis.gouv.fr/booking/create/9845')
        checkbox = driver.find_element_by_xpath("//input[@type='checkbox']")
        checkbox.click()
        next = driver.find_element_by_xpath("//input[@name='nextButton']")
        next.click()
        try:
            randevu = driver.find_elements_by_xpath("//p[@class='Bligne']")
            if len(randevu) == 0:
                print("not available")
                s.enter(10, 1, do_something, (s,))
            for i in randevu:
                global msg
                msg += i.text + '\n'
                print("sent")
                print(i.text)
            server.sendmail(sender_email, rec_email, msg.encode('utf-8'))
        except:
            print("not available")


s.enter(1, 1, do_something, (s,))
s.run()
