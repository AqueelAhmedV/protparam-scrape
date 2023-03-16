import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

url = "https://web.expasy.org/protparam/"
sequence = "FLPFQQFGRDIA"

driver = webdriver.Chrome(ChromeDriverManager().install())

wait = WebDriverWait(driver, 10)

driver.get('https://web.expasy.org/protparam/')

seq_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sib_body"]/form/textarea')))

seq_field.send_keys(sequence)

time.sleep(3)
submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sib_body"]/form/p[1]/input[2]')))
submit_btn.click()

data_div = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sib_body"]/pre[2]')))

page_source = driver.page_source

soup = BeautifulSoup(page_source, 'lxml')

print(soup)

