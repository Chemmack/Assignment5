# Program Name: Assignment5.py
# Course: IT3883/Section W01Fall Semester 2026
# Student Name: Che Mack
# Assignment Number: 5
# Due Date: 11/20/2026
# Purpose: Create a SQLite database and store temperature readings from a
# text file. Use SQL to calculate and print the average temperature for
# Sunday and Thursday.
# Resources: Instructor-provided assignment instructions and
# Assignment5input (1).txt; OpenAI ChatGPT for coding assistance.

import sqlite3
from pathlib import Path


def main():
    # Locate the input file and database beside this Python program.
    program_folder = Path(__file__).resolve().parent
    input_file = program_folder / "Assignment5input (1).txt"
    database_file = program_folder / "Assignment5.db"

    # Read each line, separating the day from its floating-point reading.
    readings = []
    with input_file.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                day, temperature = line.split()
                readings.append((day, float(temperature)))

    # Connecting creates the SQLite database if it does not already exist.
    connection = sqlite3.connect(database_file)
    try:
        with connection:
            # SQLite TEXT stores strings, and REAL stores float values.
            connection.execute("""
                CREATE TABLE IF NOT EXISTS Temperatures (
                    ID INTEGER PRIMARY KEY,
                    Day_Of_Week TEXT,
                    Temperature_Value REAL
                )
            """)

            # Refresh the readings so rerunning does not duplicate the data.
            connection.execute("DELETE FROM Temperatures")

            # Insert all readings using placeholders; SQLite assigns each ID.
            connection.executemany("""
                INSERT INTO Temperatures (Day_Of_Week, Temperature_Value)
                VALUES (?, ?)
            """, readings)

            print(f"Temperature readings loaded: {len(readings)}")

            # Calculate each average in SQL and display two decimal places.
            for day in ("Sunday", "Thursday"):
                result = connection.execute("""
                    SELECT AVG(Temperature_Value)
                    FROM Temperatures
                    WHERE Day_Of_Week = ?
                """, (day,))
                average = result.fetchone()[0]
                if average is None:
                    print(f"Average temperature for {day}: No readings found")
                else:
                    print(f"Average temperature for {day}: {average:.2f}")
    finally:
        # Always close the database connection when finished.
        connection.close()


if __name__ == "__main__":
    main()
