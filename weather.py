import requests
from tabulate import tabulate
from datetime import datetime
import sqlite3

# Constants for the base URL and API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/'
API_KEY = '9899e5d79bc6e5993d70cdb1dced0ac1'

# Create a connection to the SQLite database file
conn = sqlite3.connect('weather.db')
cursor = conn.cursor()

# Create necessary tables in the database if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS current_weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_name TEXT,
        temperature_f REAL,
        humidity INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS forecast (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_name TEXT,
        date TEXT,
        temperature_f REAL,
        humidity INTEGER
    )
''')

# Function to get weather data for a given city and store it in the database
def get_weather_data(city_name, conn, cursor):
    response = requests.get(f'{BASE_URL}weather?q={city_name}&appid={API_KEY}')
    data = response.json()
    if 'main' in data:
        temperature_f = kelvin_to_fahrenheit(data['main']['temp'])
        humidity = data['main']['humidity']

        cursor.execute('''
            INSERT INTO current_weather (city_name, temperature_f, humidity)
            VALUES (?, ?, ?)
        ''', (city_name, temperature_f, humidity))

        conn.commit()

        return data
    else:
        return None

# Function to get forecast data for a given city and store it in the database
def get_forecast_data(city_name, num_days):
    response = requests.get(f'{BASE_URL}forecast?q={city_name}&appid={API_KEY}')
    data = response.json()
    if 'list' in data:
        forecast_list = []

        for item in data['list'][:num_days]:
            date = item['dt_txt']
            temperature_f = kelvin_to_fahrenheit(item['main']['temp'])
            humidity = item['main']['humidity']

            forecast_list.append([city_name, date, temperature_f, humidity])

        cursor.executemany('''
            INSERT INTO forecast (city_name, date, temperature_f, humidity)
            VALUES (?, ?, ?, ?)
        ''', forecast_list)

        conn.commit()

        return data['list'][:num_days]
    else:
        return None

# Function to get hourly forecast data for a given city
def get_hourly_forecast_data(city_name):
    response = requests.get(f'{BASE_URL}forecast?q={city_name}&appid={API_KEY}')
    data = response.json()
    if 'list' in data:
        return data['list'][:8]  # Take the first 8 records for 24 hours
    else:
        return None

# Function to convert temperature from Kelvin to Fahrenheit
def kelvin_to_fahrenheit(temp_k):
    return round((temp_k - 273.15) * 9 / 5 + 32, 2)

# Function to get outfit recommendation based on temperature in Fahrenheit
def get_outfit_recommendation(temp_f):
    if temp_f <= 32:
        return "Heavy coat, hat, gloves, and scarf"
    elif 32 < temp_f <= 50:
        return "Coat, hat and gloves"
    elif 50 < temp_f <= 68:
        return "Jacket or sweater"
    elif 68 < temp_f <= 86:
        return "Shorts and a t-shirt"
    else:
        return "Shorts, t-shirt and stay hydrated"

# Main function to handle user interaction and options
def main():
    while True:
        print("Welcome to SkyScope. Please choose an option:")
        print("1. Get current weather data.")
        print("2. Get forecast data for specified number of days.")
        print("3. Get sunrise and sunset times.")
        print("4. Get outfit recommendation.")
        print("5. Get 3-hour forecast for the current day.")
        print("6. Stop")
        option = input()

        if option == '1':
            city_name = input("Enter the city name: ")
            weather_data = get_weather_data(city_name, conn, cursor)
            if weather_data:
                headers = ["City Name", "Temperature (F)", "Humidity"]
                data_formatted = [
                    [
                        weather_data['name'],
                        kelvin_to_fahrenheit(weather_data['main']['temp']),
                        weather_data['main']['humidity']
                    ]
                ]
                print(tabulate(data_formatted, headers=headers))
            else:
                print("Error: Failed to retrieve weather data for the specified city.")

        elif option == '2':
            city_name = input("Enter the city name: ")
            num_days = int(input("Enter the number of forecast days: "))
            forecast_data = get_forecast_data(city_name, num_days)
            if forecast_data:
                forecast_list = []
                headers = ["Date", "Temperature (F)", "Humidity"]
                for item in forecast_data:
                    date = item['dt_txt']
                    temp_fahrenheit = kelvin_to_fahrenheit(item['main']['temp'])
                    humidity = item['main']['humidity']
                    forecast_list.append([date, temp_fahrenheit, humidity])
                print(tabulate(forecast_list, headers=headers))
            else:
                print("Error: Failed to retrieve forecast data for the specified city.")

        elif option == '3':
            city_name = input("Enter the city name: ")
            cursor.execute('''
                SELECT sunrise, sunset
                FROM current_weather
                WHERE city_name = ?
            ''', (city_name,))
            data = cursor.fetchone()

            if data:
                sunrise, sunset = data
                print(f"Sunrise (UTC): {sunrise}\nSunset (UTC): {sunset}")
            else:
                print("Error: Failed to retrieve sunrise and sunset times for the specified city.")

        elif option == '4':
            city_name = input("Enter the city name: ")
            weather_data = get_weather_data(city_name, conn, cursor)
            if weather_data:
                temp_fahrenheit = kelvin_to_fahrenheit(weather_data['main']['temp'])
                outfit = get_outfit_recommendation(temp_fahrenheit)
                print(f"Outfit recommendation for current weather ({temp_fahrenheit}°F): {outfit}")
            else:
                print("Error: Failed to retrieve weather data for the specified city.")

        elif option == '5':
            city_name = input("Enter the city name: ")
            forecast_data = get_hourly_forecast_data(city_name)
            if forecast_data:
                formatted_list = []
                headers = ["Date", "Temperature (F)", "Humidity"]
                for item in forecast_data:
                    date = item['dt_txt']
                    temp_fahrenheit = kelvin_to_fahrenheit(item['main']['temp'])
                    humidity = item['main']['humidity']
                    formatted_list.append([date, temp_fahrenheit, humidity])
                print(tabulate(formatted_list, headers=headers))
            else:
                print("Error: Failed to retrieve hourly forecast data for the specified city.")

        elif option == '6':
            print("Exiting the program...")
            conn.close()
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
