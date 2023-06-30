# Weather Information System

This program allows users to retrieve weather data, including current weather, forecast, sunrise and sunset times, hourly forecast, and outfit recommendations based on temperature.

## Installation

1. Clone the repository or download the `weather.py` file.
2. Install the required dependencies by running the following command:

```shell
pip install requests tabulate
```

3. Run the program using the following command:

```shell
python weather.py
```

## Usage

1. Upon running the program, a menu will be displayed with the following options:
- Get current weather data
- Get forecast data for specified number of days
- Get sunrise and sunset times
- Get outfit recommendation
- Get 3-hour forecast for the current day
- Stop the program
2. Choose an option by entering the corresponding number and follow the prompts.
3. The program will retrieve and display the requested weather information.

## Files

- `weather.py`: Contains the main program logic for retrieving weather information and user interaction.
- `view_current_weather.py`: Retrieves and displays the current weather data stored in the database.
- `test_cases.py`: Contains unit tests for the temperature conversion and outfit recommendation functions.

## Database

The program uses an SQLite database (`weather.db`) to store the weather data. Two tables are created in the database:

1. `current_weather`: Stores the current weather data for different cities.
2. `forecast`: Stores the forecast data for different cities and dates.

