from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
import time
import csv

BLOOD_GROUP = 'A2B+'
STATE = 'Uttar Pradesh'

def extract_mobile_numbers(soup):
    rows = soup.find('table', {"id": "dgBloodDonorResults"}).find_all('span')
    mobile_numbers = [span.get_text() for span in rows if 'lblMobileNumber' in span.get('id', '')]
    return mobile_numbers

def go_to_next_page(driver, current_page):
    try:
        # Find the link for the next page and click it
        next_page = driver.find_element(By.LINK_TEXT, str(current_page + 1))
        next_page.click()
        time.sleep(3)  # Allow time for the page to load
        return True
    except:
        # No more pages available
        return False

def load_new_pages(driver):
    try:
        # Find the link for the next page (the "..." button) and click it
        next_page = driver.find_element(By.LINK_TEXT, '...')
        next_page.click()
        time.sleep(3)  # Allow time for the page to load
        return True
    except:
        # No more pages available
        return False


driver = webdriver.Chrome()
driver.get("https://www.friends2support.org/index.aspx")
driver.implicitly_wait(10)

# Select Blood Group
blood_group_dropdown = Select(driver.find_element(By.NAME, 'dpBloodGroup'))
blood_group_dropdown.select_by_visible_text(BLOOD_GROUP)

# Select Country
country_dropdown = Select(driver.find_element(By.NAME, 'dpCountry'))
country_dropdown.select_by_visible_text('INDIA')

# Wait for the state dropdown to be populated (up to 20 seconds)
state_dropdown = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "dpState"))
)

# Select the state (Uttar Pradesh)
state_select = Select(driver.find_element(By.ID, 'dpState'))
state_select.select_by_visible_text(STATE)

time.sleep(5)  # Wait for the city dropdown to populate

# Click the Search Donor button
btn = driver.find_element(By.ID, 'btnSearchDonor')
btn.click()

# Initialize a set to store unique mobile numbers
all_mobile_numbers = set()

# Start pagination from the first page
current_page = 1
pageload = False
while True:
    # Get the page source and parse it with BeautifulSoup
    html_content = driver.page_source
    soup = bs(html_content, "html.parser")
    
    # Extract mobile numbers from the current page
    mobile_numbers = extract_mobile_numbers(soup)
    all_mobile_numbers.update(mobile_numbers)  # Add to the set
    
    # Try to go to the next page
    if not go_to_next_page(driver, current_page):
        if not pageload:
            load_new_pages(driver)  # Click the "..." link to load more pages
            pageload = True
        else: 
            break
    
    current_page += 1

# Write all unique mobile numbers to a CSV file
filename = "data/" + STATE + "_" + BLOOD_GROUP + ".csv"


with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for number in all_mobile_numbers:
        writer.writerow([number]) 

print(all_mobile_numbers)

driver.quit()
