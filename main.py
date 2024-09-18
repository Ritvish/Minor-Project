from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
import time
import csv

#BLOOD_GROUPS = [
# #     'A+', 'A-', 'A1+', 'A1-', 'A1B+', 'A1B-', 'A2+', 'A2-', 'A2B+', 'A2B-', 'AB+', 'AB-', 
# #     'B+', 'B-', 'Bombay Blood Group', 'INRA', 'O+', 'O-'
# # ]

BLOOD_GROUPS = ['A1B+']

# List of all states in India
# STATES = [
#     'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 
#     'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 
#     'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 
#     'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 
#     'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
# ]
STATES = ['Kerala']

def extract_names_and_mobile_numbers(soup):
    # Find rows in the table with donor details
    rows = soup.find('table', {"id": "dgBloodDonorResults"}).find_all('tr')[1:]  # Skip header row
    name_number_pairs = []
    
    for row in rows:
        # Extract name with error handling
        name_span = row.find('span', id=lambda x: x and 'lblFullName' in x)
        name = name_span.get_text(strip=True) if name_span else 'N/A'  # Use 'N/A' if not found
        
        # Extract mobile number with error handling
        mobile_span = row.find('span', id=lambda x: x and 'lblMobileNumber' in x)
        mobile = mobile_span.get_text(strip=True) if mobile_span else 'N/A'  # Use 'N/A' if not found
        
        name_number_pairs.append((name, mobile))
    
    return name_number_pairs


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

# Setup WebDriver
driver = webdriver.Chrome()
driver.get("https://www.friends2support.org/index.aspx")
driver.implicitly_wait(10)

# Loop over all blood groups and states
for BLOOD_GROUP in BLOOD_GROUPS:
    for STATE in STATES:
        print(f"Processing Blood Group: {BLOOD_GROUP}, State: {STATE}")

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

        # Select the state
        state_select = Select(driver.find_element(By.ID, 'dpState'))
        state_select.select_by_visible_text(STATE)

        time.sleep(5)  # Wait for the city dropdown to populate

        # Click the Search Donor button
        btn = driver.find_element(By.ID, 'btnSearchDonor')
        btn.click()

        # Initialize a set to store unique name-number pairs
        all_name_number_pairs = set()

        # Start pagination from the first page
        current_page = 1
        pageload = False
        while True:
            # Get the page source and parse it with BeautifulSoup
            html_content = driver.page_source
            soup = bs(html_content, "html.parser")

            # Extract name-number pairs from the current page
            name_number_pairs = extract_names_and_mobile_numbers(soup)
            all_name_number_pairs.update(name_number_pairs)  # Add to the set

            # Try to go to the next page
            if not go_to_next_page(driver, current_page):
                if not pageload:
                    load_new_pages(driver)  # Click the "..." link to load more pages
                    pageload = True
                else: 
                    break

            current_page += 1

        # Write all unique name-number pairs to a CSV file
        filename = "data/" + STATE + "_" + BLOOD_GROUP + ".csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Mobile Number"])  # Add headers
            for name, number in all_name_number_pairs:
                writer.writerow([name, number])

        print(f"Completed Blood Group: {BLOOD_GROUP}, State: {STATE}")

driver.quit()
