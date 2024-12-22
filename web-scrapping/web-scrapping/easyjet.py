from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the web driver
driver = webdriver.Chrome()  # Replace with your web driver (e.g., `webdriver.Firefox()`)

try:
    # Navigate to EasyJet's website
    driver.get("https://www.easyjet.com/en")

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "from")))

    # Enter departure airport
    departure = driver.find_element(By.ID, "from")
    departure.send_keys("London (All Airports)")
    time.sleep(2)
    departure.send_keys(Keys.RETURN)

    # Enter arrival airport
    arrival = driver.find_element(By.ID, "to")
    arrival.send_keys("SOF")
    time.sleep(2)
    arrival.send_keys(Keys.RETURN)

    # Select departure date
    date_picker = driver.find_element(By.ID, "when")
    date_picker.send_keys('18/11/2024 - One way')
    time.sleep(2)

    # Select a date (example: select the 15th of the next month)
    next_month_button = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-next")
    next_month_button.click()
    time.sleep(1)
    date = driver.find_element(By.XPATH, "//a[text()='15']")
    date.click()

    # Submit the search
    search_button = driver.find_element(By.ID, "search-button")
    search_button.click()

    # Wait for search results to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results")))

    # Print search results (basic example)
    results = driver.find_elements(By.CLASS_NAME, "search-result")
    for result in results:
        print(result.text)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the browser
    driver.quit()
