import psycopg2
from psycopg2.extras import execute_values
import pandas as pd

# Database connection details
DB_HOST = 'localhost'
DB_NAME = 'amr-global'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'


# Function to create a connection to the PostgreSQL database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Database connection established.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise


# Function to create a table if it doesn't exist
def create_table_if_not_exists(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS flight_data (
        id SERIAL PRIMARY KEY,
        date DATE,
        status TEXT,
        start_location TEXT,
        end_location TEXT,
        flight_number TEXT,
        departure_time TEXT,
        arrival_time TEXT,
        flight_duration TEXT,
        departure_location TEXT,
        arrival_location TEXT,
        price TEXT,
        website TEXT,
        url TEXT
    );
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
            print("Table ensured in the database.")
    except Exception as e:
        print(f"Error creating table: {e}")
        connection.rollback()
        raise


# Function to upload data to PostgreSQL
def upload_to_postgres(connection, df):
    insert_query = """
    INSERT INTO flight_data (
        date, status, start_location, end_location, flight_number, departure_time,
        arrival_time, flight_duration, departure_location, arrival_location,
        price, website, url
    ) VALUES %s
    """
    # Prepare data for bulk insertion
    values = [
        (
            row['Date'],
            row['Status'],
            row['Start Location'],
            row['End Location'],
            row['Flight Number'],
            row['Departure Time'],
            row['Arrival Time'],
            row['Flight Duration'],
            row['Departure Location'],
            row['Arrival Location'],
            row['Price'],
            row['Website'],
            row['URL']
        )
        for _, row in df.iterrows()
    ]

    try:
        with connection.cursor() as cursor:
            execute_values(cursor, insert_query, values)
            connection.commit()
            print(f"{len(values)} records inserted successfully.")
    except Exception as e:
        print(f"Error uploading data to the database: {e}")
        connection.rollback()
        raise


# Main function to scrape, save, and upload data
def raynair_data():
    start_date, end_date = get_date_range()  # Get today's date and the next 14 days
    starting_locations = ['BHX', 'STN']  # You can change this to other locations if needed
    flight_data = collect_flight_data(start_date, end_date, starting_locations)
    df = create_dataframe(flight_data)
    print(df)

    # Save to CSV
    df.to_csv('flight_data.csv', index=False)
    print("Data saved to flight_data.csv")

    # Upload to PostgreSQL
    connection = None
    try:
        connection = connect_to_db()
        create_table_if_not_exists(connection)
        upload_to_postgres(connection, df)
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")


# Run the script
raynair_data()
