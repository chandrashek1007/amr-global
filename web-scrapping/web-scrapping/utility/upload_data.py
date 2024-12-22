import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from backend.utils.database import get_db, engine
from backend.models.flight import FlightMaster

# File path to the CSV file
CSV_FILE_PATH = "flight_data.csv"

# Read the CSV file into a DataFrame
def load_csv_to_dataframe(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

# Insert data into the FlightMaster table
def upload_data_to_table(df, session):
    try:

        # Iterate over rows in the DataFrame and insert into the table
        for _, row in df.iterrows():
            flight = FlightMaster(
                created_at=datetime.now(),
                updated_at=datetime.now(),
                status=row['Status'],
                start_location=row['Start Location'],
                end_location=row['End Location'],
                flight_number=row['Flight Number'],
                departure_date_time=datetime.strptime(f"{row['Date']} {row['Departure Time']}", "%d/%m/%Y %H:%M"),
                arrival_date_time=datetime.strptime(f"{row['Date']} {row['Arrival Time']}", "%d/%m/%Y %H:%M"),
                flight_duration=row['Flight Duration'] if pd.notna(row['Flight Duration']) else '00h 00m',
                departure_location=row['Departure Location'],
                arrival_location=row['Arrival Location'],
                price=float(str(row['Price']).replace('£','')),
                website=row['Website'],
                url=row['URL']
            )
            session.add(flight)
        session.commit()
        print("Data uploaded successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error uploading data to the table: {e}")

# Main function
def main():
    # Load the CSV data
    df = load_csv_to_dataframe(CSV_FILE_PATH)
    if df is None:
        print("Failed to load data from CSV file.")
        return

    # Create a session
    with Session(engine) as session:
        upload_data_to_table(df, session)

if __name__ == "__main__":
    main()
