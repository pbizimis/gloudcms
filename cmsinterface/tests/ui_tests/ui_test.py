from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

service = Service('/home/philip/chromedriver.exe')
service.start()
driver = webdriver.Remote(service.service_url)

driver.get('https://www.google.nl/')
delay = 10

driver.get("http://127.0.0.1:8080")
assert "Gloud" in driver.title

driver.find_element_by_partial_link_text("Login with").click()
elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'identifier')))
elem.send_keys("gloudtest123@gmail.com")
elem.send_keys(Keys.RETURN)
pw = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.NAME, 'password')))
pw.click()
pw.send_keys("CODE123@")
pw.send_keys(Keys.RETURN)
WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT , 'Erweitert'))).click()
WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT , 'GloudCMS'))).click()
WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID , 'submit_approve_access'))).click()
articles = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR  , 'a[href="articles"]')))
assert "Dashboard" in driver.title

articles.click()
assert "Articles" in driver.title

upsert = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID  , 'link-to-doc')))
upsert.click()
upsert.send_keys("https://docs.google.com/document/d/1D4oBVZ0_BjjNQ9KqfNAtTLLLZfY_nvH2c6gf2H7zjzE/edit")
upsert.send_keys(Keys.RETURN)
success = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID  , 'success-link')))
assert success.text == "Editor Template (Created)"

upsert.clear()
upsert.send_keys("https://docs.google.com/document/d/1D4oBVZ0_BjjNQ9KqfNAtTLLLZfY_nvH2c6gf2H7zjzE/edit")
upsert.send_keys(Keys.RETURN)
success = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID  , 'success-link')))
assert success.text == "Editor Template (Updated)"

upsert.clear()
upsert.send_keys("https://docs.gooNAtTLLLZfY_nvH2c6gf2H7zjzE/edit")
upsert.send_keys(Keys.RETURN)
error = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID  , 'error-link')))
assert error.text == "Wrong Document Link!"

upsert.clear()
upsert.send_keys("https://docs.google.com/document/d/1iwr0svUf4eFpBDwI-ZslJrMYz3u0290PZHbN-GxZtsg/edit")
upsert.send_keys(Keys.RETURN)
time.sleep(2)
sec_error = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID  , 'error-link')))
assert sec_error.text == "You have no permissions for this document!"

upsert.clear()
upsert.send_keys("https://docs.google.com/document/d/1kQtFp38VkC0kapzUkZtRhcxjmPKjVG3VK8gXThJ4S0c/edit")
upsert.send_keys(Keys.RETURN)
time.sleep(2)
error = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID  , 'error-link')))
assert error.text == "Wrong template!"

delete = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID  , 'url-to-doc')))
delete.click()
delete.send_keys("editor_template")
delete.send_keys(Keys.RETURN)
success = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID  , 'success-aurl')))
assert success.text == "Deleted Article with URL: editor_template"

delete.clear()
delete.send_keys("editor_template")
delete.send_keys(Keys.RETURN)
time.sleep(2)
error = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID  , 'success-aurl')))
assert error.text == "Article with URL: editor_template not found!"
