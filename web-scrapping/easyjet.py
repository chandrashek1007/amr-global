import requests
from datetime import datetime
import sys


def get_max_bookable_date(dest, origin):
    # Validate the input parameters
    if not dest:
        print("Error: missing 'dest' parameter")
        return
    if not origin:
        print("Error: missing 'origin' parameter")
        return

    # Prepare today's date in the required format
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Set up the request parameters
    url = 'https://www.easyjet.com/ejcms/nocache/api/lowestfares/get/'
    params = {
        'destinationIata': dest,
        'displayCurrencyId': '0',
        'languageCode': 'en-US',
        'originIata': origin,
        'startDate': today_str
    }
    headers = {
        'cache-control': 'no-cache',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, sdch, br'
    }

    # Make the API request
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print("Error making request:", e)
        return

    # Process the response to find the farthest available date
    farthest_date = datetime.now()
    for month in data.get('months', []):
        year = month['year']
        month_num = month['month'] - 1  # Adjust for 0-based month indexing in datetime
        for day_obj in month.get('days', []):
            if day_obj['flightStatus'] > 0:
                date = datetime(year, month_num + 1, day_obj['day'])
                if date > farthest_date:
                    farthest_date = date

    # Display the farthest available date
    print("Farthest bookable date:", farthest_date.strftime("%Y-%m-%d"))


# Input Parameters
if __name__ == "__main__":
    # Either provide dest and origin as arguments or directly in the code
    if len(sys.argv) == 3:
        dest = sys.argv[1]
        origin = sys.argv[2]
    else:
        dest = input("Enter destination IATA code: ")
        origin = input("Enter origin IATA code: ")

    get_max_bookable_date(dest, origin)
