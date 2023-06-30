import sqlite3
from tabulate import tabulate

# Create a connection to the SQLite database file
conn = sqlite3.connect('weather.db')
cursor = conn.cursor()

# Execute a SELECT query to retrieve data from the current_weather table
cursor.execute('SELECT * FROM current_weather')

# Fetch all the rows from the result
rows = cursor.fetchall()

# Display the data in a tabular format
if rows:
    headers = ["ID", "City Name", "Temperature (F)", "Humidity"]
    data_formatted = []
    for row in rows:
        data_formatted.append(row)
    print(tabulate(data_formatted, headers=headers))
else:
    print("No data available in the current_weather table.")

# Close the database connection
conn.close()
