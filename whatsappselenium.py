from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\LENOVO\AppData\Local\Google\Chrome\User Data")  
# options.add_argument(r'--profile-directory=Person 1')
driver = webdriver.Chrome(options=options)
time.sleep(15)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
# driver.get("https://web.whatsapp.com")
driver.get("https://youtube.com")


# # Function to send a message
# def send_message(phone_number, message):
#     search_box = driver.find_element(By.CSS_SELECTOR, "div[title='Search input textbox']")
#     search_box.click()
#     search_box.send_keys(phone_number)
#     time.sleep(2)  # Wait for the contact to appear
#     search_box.send_keys(Keys.ENTER)

#     message_box = driver.find_element(By.CSS_SELECTOR, "div[title='Type a message']")
#     message_box.click()
#     message_box.send_keys(message)
#     message_box.send_keys(Keys.ENTER)

# # List of phone numbers and message
# phone_numbers = ["+919540240000", "+919717103354"]
# message = "test1223"

# # Send messages
# for phone_number in phone_numbers:
#     send_message(phone_number, message)
#     time.sleep(2)  # Wait a bit before sending the next message

# Close the WebDriver
driver.quit()
