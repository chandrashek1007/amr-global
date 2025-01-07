import re
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Initialize the Selenium WebDriver with options
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(5)
    return driver


# Calculate today's date and next week's date range
def get_date_range():
    today = datetime.today()
    start_date = today  # Today
    end_date = today + timedelta(days=14)  # 14
    return start_date, end_date
# Construct the URL for the Ryanair flight search page
def construct_url(start_location, date):
    date_input = date.strftime("%Y-%m-%d")
    return f"https://www.ryanair.com/gb/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut={date_input}&dateIn=&isConnectedFlight=false&discount=0&isReturn=false&promoCode=&originIata={start_location}&destinationIata=SOF&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate={date_input}&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata={start_location}&tpDestinationIata=SOF"


# Extract flight data from a given page URL
def scrape_flight_data(driver, url):
    driver.get(url)
    flight_data = []

    try:
        price_elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'flight-card-summary__new-value'))
        )
        info_elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'flight-info__time'))
        )
        flight_num_elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-flight-num__content'))
        )
        flight_duration_elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-ref="flight_duration"]'))
        )

        # Extract text content
        prices = [element.text for element in price_elements]
        info_texts = [element.text for element in info_elements]
        flight_nums = [element.text for element in flight_num_elements]
        flight_durations = [element.text.strip() for element in flight_duration_elements]

        for j in range(len(prices)):
            idx = j * 2
            departure_info = info_texts[idx].split('\n')
            arrival_info = info_texts[idx + 1].split('\n')
            flight_data.append({
                'Price': prices[j],
                'Flight Number': flight_nums[j],
                'Flight Duration': flight_durations[j],
                'Departure Time': departure_info[0],
                'Departure Location': departure_info[1],
                'Arrival Time': arrival_info[0],
                'Arrival Location': arrival_info[1]
            })

    except Exception as e:
        print(f"Error retrieving data from {url}: {e}")

    return flight_data


# Collect data for multiple dates and locations
def collect_flight_data(start_date, end_date, starting_locations):
    driver = init_driver()
    all_flight_data = []

    try:
        for start_location in starting_locations:
            current_date = start_date
            while current_date <= end_date:
                url = construct_url(start_location, current_date)
                flight_data = scrape_flight_data(driver, url)

                for data in flight_data:
                    data.update({
                        'Date': current_date.strftime("%d/%m/%Y"),
                        'Start Location': start_location,
                        'End Location': "SOF",
                        'Website': "Ryanair",
                        'Status': "FromUK",
                        'URL': url
                    })
                    all_flight_data.append(data)

                current_date += timedelta(days=1)

    finally:
        driver.quit()

    return all_flight_data


# Convert the collected data into a DataFrame
def create_dataframe(flight_data):
    return pd.DataFrame(flight_data, columns=[
        'Date', 'Status', 'Start Location', 'End Location', 'Flight Number',
        'Departure Time', 'Arrival Time', 'Flight Duration', 'Departure Location',
        'Arrival Location', 'Price', 'Website', 'URL'
    ])


# Main function to run the full scraping process
def raynair_data():
    start_date, end_date = get_date_range()  # Get today's date and the next 6 days
    starting_locations = ['BHX', 'STN']  # You can change this to other locations if needed
    flight_data = collect_flight_data(start_date, end_date, starting_locations)
    df = create_dataframe(flight_data)
    print(df)
    df.to_csv('flight_data.csv', index=False)  # Save data to CSV


# Run the script
raynair_data()
