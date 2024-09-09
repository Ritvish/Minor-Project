from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
import time

driver = webdriver.Chrome()

driver.get("https://www.friends2support.org/index.aspx")
driver.implicitly_wait(10)

# Select Blood Group
blood_group_dropdown = Select(driver.find_element(By.NAME, 'dpBloodGroup'))
blood_group_dropdown.select_by_visible_text('A+')

# Select Country
country_dropdown = Select(driver.find_element(By.NAME, 'dpCountry'))
country_dropdown.select_by_visible_text('INDIA')

# Wait for the state dropdown to be populated (up to 20 seconds)
state_dropdown = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "dpState"))
)

# Select the state (Delhi)
state_select = Select(driver.find_element(By.ID, 'dpState'))
state_select.select_by_visible_text('Delhi')

time.sleep(5)  # Wait for the city dropdown to populate

# Click the Search Donor button
btn = driver.find_element(By.ID, 'btnSearchDonor')
btn.click()

# Get the page source and parse it with BeautifulSoup
html_content = driver.page_source
soup = bs(html_content, "html.parser")

# Find all <tr> tags
rows = soup.find_all('tr')

# Loop through the rows and extract phone numbers
for row in rows:
    # Find all <td> tags in the row
    columns = row.find_all('td')
    
    # Assuming the phone number is in the 4th <td> (index 3)
    if len(columns) > 3:
        phone_number = columns[3].text.strip()  # Extract and clean the phone number text
        if phone_number:  # If the phone number is not empty, print it
            print(phone_number)

time.sleep(10)  # this is to observe the result, you can remove this later

driver.quit()