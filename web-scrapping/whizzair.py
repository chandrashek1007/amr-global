import re

text = """London
Sofia
Total journey length:03h 10min Direct flight
08:45
20 Nov
Luton (LTN)
London, United Kingdom
Nearby airport
Flight duration: 03h 10min
|
Flight number: W6 4302
Wizz Air
13:55
20 Nov
Sofia Airport (SOF)
Sofia, Bulgaria"""

pattern = r"(?P<from_city>[A-Za-z]+)\s(?P<to_city>[A-Za-z]+)\sTotal journey length:(?P<total_length>\d{2}h \d{2}min)\sDirect flight\n(?P<departure_time>\d{2}:\d{2})\n(?P<departure_date>\d{2} \w+)\n(?P<departure_airport>[A-Za-z\s\(\)]+)\n(?P<departure_country>[A-Za-z\s,]+)\nNearby airport\nFlight duration:\s(?P<flight_duration>\d{2}h \d{2}min)\s\|\nFlight number:\s(?P<flight_number>[A-Z0-9 ]+)\n(?P<airline>[A-Za-z\s]+)\n(?P<arrival_time>\d{2}:\d{2})\n(?P<arrival_date>\d{2} \w+)\n(?P<arrival_airport>[A-Za-z\s\(\)]+)\n(?P<arrival_country>[A-Za-z\s,]+)"

match = re.search(pattern, text)
if match:
    details = match.groupdict()
    print(details)
