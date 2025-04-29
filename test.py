from selenium import webdriver
from RecaptchaSolver import RecaptchaSolver
import time
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import csv
from requests_html import HTMLSession
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver options
options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--log-level=3")
options.add_argument('--no-proxy-server')
options.add_argument("--incognito")
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
# driver.get("https://www.google.com/recaptcha/api2/demo")
driver.get("https://www.wcb.ny.gov/icpocinq/icpocsearch.jsp")

recaptchaSolver = RecaptchaSolver(driver)

try:
    # Perform CAPTCHA solving
    t0 = time.time()
    driver.find_element(By.ID, "subACK").click()
    driver.find_element(By.NAME, "submit").click()
    
    recaptchaSolver.solveCaptcha()
    time.sleep(3)
    driver.find_element(By.NAME, "empName").send_keys('ayz')
    driver.find_element(By.NAME, "submit").click()
    print(f"Time to solve the captcha: {time.time() - t0:.2f} seconds")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'emptable'))
    )
    
    # driver.get("https://www.w3schools.com/html/html_tables.asp")
    # driver.get("https://www.wcb.ny.gov/icpocinq/icpocempsrch.jsp")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table",{"id":"emptable"}) # to select the right table
    
    print("table")
    print(table)
    rows = table.findAll('tr')

    # strip the header from rows
    headers = rows[0]
    header_text = []

    # add the table header text to array
    for th in headers.findAll('th'):
        header_text.append(th.text)

    # init row text array
    row_text_array = []

    # loop through rows and add row text to array
    for row in rows[1:]:
        row_text = []
        # loop through the elements
        for row_element in row.findAll(['th', 'td']):
            # append the array with the elements inner text
            row_text.append(row_element.text.replace('\n', '').strip())
        # append the text array to the row text array
        row_text_array.append(row_text)

    with open("out.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(header_text)
        for row_text_single in row_text_array:
            wr.writerow(row_text_single) 
        
except Exception as e:
    print(f"An error occurred: {e}")
    driver.quit()