import re
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Initialize the Selenium WebDriver with options
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(5)
    return driver

def get_date_range():
    today = datetime.today()
    start_date = today  # Today
    end_date = today + timedelta(days=14)  # 14
    return start_date, end_date
# Construct the URL for the Ryanair flight search page
def construct_url(start_location, date):
    date_input = date.strftime("%Y-%m-%d")
    return "https://www.esky.com/flights/search/ap/BHX/ap/SOF?departureDate=2024-11-20&pa=1&py=0&pc=0&pi=0&sc=economy&filters=%7B%22Transfers%22:%5B%22None%22%5D%7D"

# Extract flight data from a given page URL
def scrape_flight_data(driver, url):
    driver.get(url)
    flight_data = []

    try:
        # price_elements = WebDriverWait(driver, 15).until(
        #     EC.presence_of_all_elements_located((By.CLASS_NAME, 'flights-list ng-star-inserted'))
        # )
        flight_list_container = driver.find_element(By.TAG_NAME, 'so-fsr-flights-list')

        flight_list_div = flight_list_container.find_elements(By.TAG_NAME, 'so-fsr-flight-block')


        for ele in flight_list_div:
            ele.find_element(By.TAG_NAME, 'ecs-button').click()
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "so-fsr-middle-step-flight-details"))
                )

                flight_details = driver.find_element(By.TAG_NAME, 'so-fsr-middle-step-flight-details').text
                print(flight_details)
                if flight_details:
                    pattern = r"(?P<from_city>[A-Za-z]+)\s(?P<to_city>[A-Za-z]+)\sTotal journey length:(?P<total_length>\d{2}h \d{2}min)\sDirect flight\n(?P<departure_time>\d{2}:\d{2})\n(?P<departure_date>\d{2} \w+)\n(?P<departure_airport>[A-Za-z\s\(\)]+)\n(?P<departure_country>[A-Za-z\s,]+)\nNearby airport\nFlight duration:\s(?P<flight_duration>\d{2}h \d{2}min)\s\|\nFlight number:\s(?P<flight_number>[A-Z0-9 ]+)\n(?P<airline>[A-Za-z\s]+)\n(?P<arrival_time>\d{2}:\d{2})\n(?P<arrival_date>\d{2} \w+)\n(?P<arrival_airport>[A-Za-z\s\(\)]+)\n(?P<arrival_country>[A-Za-z\s,]+)"

                    match = re.search(pattern, flight_details)
                    if match:
                        details = match.groupdict()
                        print(details)
                    print("Popup appeared!")
            except TimeoutException:
                print("Popup did not appear.")
        # Extract text content
        # prices = [element.text for element in price_elements]
        #
        #
        # for j in range(len(prices)):
        #     idx = j * 2
        #     departure_info = info_texts[idx].split('\n')
        #     arrival_info = info_texts[idx + 1].split('\n')
        #     flight_data.append({
        #         'Price': prices[j],
        #         'Flight Number': flight_nums[j],
        #         'Flight Duration': flight_durations[j],
        #         'Departure Time': departure_info[0],
        #         'Departure Location': departure_info[1],
        #         'Arrival Time': arrival_info[0],
        #         'Arrival Location': arrival_info[1]
        #     })

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

                # for data in flight_data:
                #     data.update({
                #         'Date': current_date.strftime("%d/%m/%Y"),
                #         'Start Location': start_location,
                #         'End Location': "SOF",
                #         'Website': "Ryanair",
                #         'Status': "FromUK",
                #         'URL': url
                #     })
                #     all_flight_data.append(data)
                #
                # current_date += timedelta(days=1)

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


def esky_data():
    start_date, end_date = get_date_range()  # Get today's date and the next 6 days
    starting_locations = ['BHX']  # You can change this to other locations if needed
    flight_data = collect_flight_data(start_date, end_date, starting_locations)
    df = create_dataframe(flight_data)
    print(df)
    df.to_csv('flight_data.csv', index=False)  #



esky_data()